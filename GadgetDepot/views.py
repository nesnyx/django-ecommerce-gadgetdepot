from django.shortcuts import render
from django.http import HttpRequest
from store.models import Product
def home(request):
    product = Product.objects.all().filter(is_available=True)
    
    return render(request, 'core/index.html', {
        'product' : product
    })