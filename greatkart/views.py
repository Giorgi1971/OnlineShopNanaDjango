from django.http.response import HttpResponse
from django.shortcuts import render

from store.models import Product

def home(request):
    products = Product.objects.filter(is_avaliable=True).order_by('-created_date')[1:9]
    context = {
        'list':products,
    }
    return render(request, 'index.html', context)