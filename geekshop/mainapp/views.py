from django.shortcuts import render
import json

from mainapp.models import Product, ProductCategory


def main(request):
    products = Product.objects.all()[:4]
    content = {
        'title': 'Главная',
        'products': products
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    same_products = Product.objects.all()[:4]
    content = {
        'title': 'Товары',
        'links_menu': links_menu,
        'same_products': same_products
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

