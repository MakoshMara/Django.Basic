from django import template

from geekshop import settings

register = template.Library()


@register.filter(name='media_for_users')
def media_for_users(path_to_avatar):
    if not path_to_avatar:
        path_to_avatar = 'users_avatars/product-11.jpg'
    return f'{settings.MEDIA_URL}{path_to_avatar}'


def media_for_products(path_to_img):
    if not path_to_img:
        path_to_img = 'products_images/default.jpg'
    return f'{settings.MEDIA_URL}{path_to_img}'

def capitalize(string):
    string = string.capitalize()
    return f'{string}'

register.filter('capitalize', capitalize)
register.filter('media_for_products', media_for_products)
