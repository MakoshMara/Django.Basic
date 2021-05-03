from django.urls import path
from adminapp import views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('user/create/', adminapp.user_create, name = 'user_create'),
    path('user/read/', adminapp.users, name = 'user_read'),
    path('user/update/<int:pk>/', adminapp.user_update, name = 'user_update'),
    path('user/delete/<int:pk>/', adminapp.user_delete, name = 'user_delete'),

    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/read/', adminapp.categories, name='category_read'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.category_delete, name='category_delete'),

    path('products/create/<int:pk>/', adminapp.products_create, name='product_create'),
    path('products/read/category/<int:pk>/', adminapp.products, name='products'),
    path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', adminapp.products_update, name='product_update'),
    path('products/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),

]