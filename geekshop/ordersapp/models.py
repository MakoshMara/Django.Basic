from django.db import models

from geekshop import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCEED, 'Отправлен в обработку'),
        (PROCEEDED, 'Oбрабатывается'),
        (PAID, 'Oплачен'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Oтменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    update = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    status = models.CharField(choices=ORDER_STATUS_CHOICES, default=FORMING, verbose_name='Статус', max_length=3)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_total_quantity(self):
        items = self.orderitem.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitem.select_related()
        return sum(list(map(lambda x: x.get_product_coast(), items)))

    def get_summary(self):
        items = self.orderitem.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price,items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def __str__(self):
        return f'Текущий заказ: {self.pk}'

    def delete(self):
        for item in self.orderitem.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem')
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    def get_product_coast(self):
        return self.quantity * self.product.price
