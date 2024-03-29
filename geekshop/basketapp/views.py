from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView

from authapp.models import ShopUser
from basketapp.models import Basket
from mainapp.models import Product


# @login_required
# def basket(request):
#     basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
#     content = {
#         'title': 'Корзина',
#         'basket_items': basket_items,
#     }
#
#     return render(request, 'basketapp/basket.html', content)

class BasketView(ListView):
    model = Basket
    template_name = 'basketapp/basket.html'

@login_required
def basket_add(request, pk):
    # if 'login' in request.META.get('HTTP_REFERER'):
    #     return HttpResponseRedirect(reverse('products:product', args=[pk]))
    # product_item = get_object_or_404(Product, pk=pk)
    # basket_item = Basket.objects.filter(product=product_item, user=request.user).first()
    #
    # if not basket_item:
    #     basket_item = Basket(user=request.user, product=product_item)
    # basket_item.quantity += 1
    # basket_item.save(update_fields=['quantity', 'product'])

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(user=request.user, product=product_item).first()

    if not basket_item:
        basket_item = Basket(user=request.user, product=product_item)
        basket_item.save()
    basket_item.quantity += 1
    basket_item.save(update_fields=['quantity', 'product'])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
            print(new_basket_item.product_cost)
        else:
            new_basket_item.delete()
        object_list = Basket.objects.filter(user=request.user).order_by('product__category')
        print(object_list)

        content = {
            'object_list': object_list
        }
        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})
