from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='category'),
    path('<int:pk>/<int:page>/', mainapp.products, name='products'),
    path('product/<int:pk>/', mainapp.product, name='product')
]

