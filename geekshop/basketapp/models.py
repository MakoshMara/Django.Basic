from django.conf import settings
from django.db import models

from mainapp.models import Product

# class BasketQuerySet(models.QuerySet):
#     def delete(self):
#         for obj in self:
#             obj.product.quantity += obj.quantity
#             obj.product.save()
#         super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    @staticmethod
    def get_item_quantity(pk):
        basket_quantity = Basket.objects.get(pk=pk).quantity
        return basket_quantity


    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()
