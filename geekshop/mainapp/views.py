import random

from django.shortcuts import render, get_object_or_404
import json

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return 0


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_product(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related()[:3]
    content = {
        'title': 'Главная',
        'products': products,
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category=category_item)

        content = {
            'title': 'Товары',
            'links_menu': links_menu,
            'products': products_list,
            'category': category_item,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)

    content = {
        'title': 'Товары',
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    content = {
        'title': 'Продукт',
        'product': get_object_or_404(Product, pk=pk),
        'links_menu': ProductCategory.objects.all(),
    }
    return render(request, 'mainapp/product.html', content)


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
        'contacts': contacts,
    }
    return render(request, 'mainapp/contact.html', content)
