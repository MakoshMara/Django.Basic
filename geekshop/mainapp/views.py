from django.shortcuts import render
import json


def main(request):
    content = {
        'title': 'Главная'
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    links_menu = [
        {'href': 'prod_all', 'name': 'все'},
        {'href': 'prod_home', 'name': 'дом'},
        {'href': 'prod_office', 'name': 'офис'},
        {'href': 'prod_modern', 'name': 'модерн'},
        {'href': 'prod_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Товары',
        'links_menu': links_menu
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

