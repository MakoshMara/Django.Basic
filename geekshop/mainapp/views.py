from django.shortcuts import render, get_object_or_404
import json

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def main(request):
    products = Product.objects.all()[:4]
    content = {
        'title': 'Главная',
        'products': products
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    basket = 0
    if request.user.is_authenticated:
        basket = sum(list(Basket.objects.filter(user = request.user).values_list('quantity',flat=True)))

    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk ==0:
            products_list = Product.objects.all().order_by('price')
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk =pk)
            products_list = Product.objects.filter(category= category_item)

        content = {
            'title': 'Товары',
            'links_menu': links_menu,
            'products': products_list,
            'category': category_item,
            'basket': basket
        }
        return render(request,'mainapp/products_list.html', content)

    same_products = Product.objects.all()[3:5]
    content = {
        'title': 'Товары',
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': basket
    }
    return render(request, 'mainapp/products.html', content)

def contact(request):
    contacts = [
        {
            "location": "Москва",
            "phone": "+7-495-8888888",
            "addr": "В пределах МКАД"
        },
        {
            "location": "Новосибирск",
            "phone": "+7-383-8888888",
            "addr": "В окодэме"
        },
        {
            "location": "Улан-Удэ",
            "phone": "+7-3012-888888",
            "addr": "У головы Ленина"
        }
    ]

    content = {
        'title': 'Контакты',
        'contacts': contacts
    }
    return render(request, 'mainapp/contact.html', content)

# Create your views here.

