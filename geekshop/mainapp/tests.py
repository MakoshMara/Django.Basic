from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command


class TestMainappSmoke(TestCase):
    success_status_code = 200

    def setUp(self):
        category = ProductCategory.objects.create(name='category 1')
        Product.objects.create(category=category, name='product 1')
        Product.objects.create(category=category, name='product 2')
        self.client = Client()


    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_status_code)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, self.success_status_code)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.success_status_code)

    def test_mainapp_product_urls(self):
        response = self.client.get(f'/products/0')
        self.assertEqual(response.status_code, self.success_status_code)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, self.success_status_code) #Так и не поняла, почему он не подставляет номер категории(( при этом же норм отрабатывает и на создание категории и на нулевой (которая "все")

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.success_status_code)

