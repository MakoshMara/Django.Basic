from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('<int:pk>', mainapp.products, name='category'),
    path('', mainapp.products, name='products'),
    path('product/<int:pk>/', mainapp.product, name='product'),
]

