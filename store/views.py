from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from carts.models import CartItem
from category.models import Category
from store.models import Product
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from django.db.models import Q

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug) 
        products = Product.objects.filter(category=categories, is_avaliable=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        p_count = products.count()
    else:
        products = Product.objects.filter(is_avaliable=True).order_by('id')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        p_count = products.count()

    context = {
        'count':p_count,
        'list':paged_products,
    }
    return render(request, 'store/store.html', context)


def ss(request):
    return render(request, 'enter.html')




def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e
    context = {'single_product':single_product, 'in_cart':in_cart}
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.POST:
        keyword = request.POST['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            p_count = products.count()

    context = {
        'list':products,
        'count':p_count,
    }
    return render(request, 'store/store.html', context)
