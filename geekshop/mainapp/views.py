import random
from django.views.decorators.cache import cache_page

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
import json

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return 0

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products_list = get_products()
    return random.sample(list(products_list), 1)[0]


def get_same_product(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    products = get_products()[:3]
    content = {
        'title': 'Главная',
        'products': products,
    }
    return render(request, 'mainapp/index.html', content)


@cache_page(3600)
def products(request, pk=None):
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            products_list = get_products_orederd_by_price()
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_category(pk)
            products_list = get_products_in_category_orederd_by_price(pk)

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
        'product': get_product(pk),
        'links_menu': get_links_menu(),
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
