from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection

def db_profile_by_type(prefix, type, queries):
   update_queries = list(filter(lambda x: type in x['sql'], queries))
   print(f'db_profile {type} for {prefix}:')
   [print(query['sql']) for query in update_queries]

@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
   if instance.pk:
       if instance.is_active:
           instance.product_set.update(is_active=True)
       else:
           instance.product_set.update(is_active=False)

       db_profile_by_type(sender, 'UPDATE', connection.queries)

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:user_read'))
    else:
        user_form = ShopUserRegisterForm()

    content = {
        'form': user_form
    }

    return render(request,'adminapp/user_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    content = {
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser,pk=pk)
    if request.method =='POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid:
            user_form.save()
            return HttpResponseRedirect(reverse('admin:user_read'))
    else:
        user_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'form': user_form
    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user_item = get_object_or_404(ShopUser,pk=pk)
    if request.method =='POST':
        if user_item.is_active:
            user_item.is_active = False
        else:
            user_item.is_active = True
        user_item.save()
        return HttpResponseRedirect(reverse('admin:user_read'))


    content = {
           'user_to_delete':user_item
       }
    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:category_read'))
    else:
        category_form = ProductCategoryEditForm()

    content = {
        'form': category_form
    }

    return render(request, 'adminapp/category_create.html', content)

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories_list = ProductCategory.objects.all().order_by('-is_active')
    content = {
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)

# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if category_form.is_valid:
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:category_read'))
#     else:
#         category_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {
#         'form': category_form
#     }
#
#     return render(request, 'adminapp/category_create.html', content)

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        if category_item.is_active:
            category_item.is_active = False
        else:
            category_item.is_active = True
        category_item.save()
        return HttpResponseRedirect(reverse('admin:category_read'))

    content = {
        'category_to_delete': category_item
    }
    return render(request, 'adminapp/category_delete.html', content)

@user_passes_test(lambda u: u.is_superuser)
def products_create(request):
    pass

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    categories_item = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category=categories_item).order_by('-is_active')
    content = {
        'objects': products_list,
        'category': categories_item
    }

    return render(request, 'adminapp/products.html', content)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        category_pk = self.get_object().pk
        context = super().get_context_data(**kwargs)
        context['category'] = category_pk
        return context

@user_passes_test(lambda u: u.is_superuser)
def products_update(request, pk):
    edit_prod = get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        update_form = ProductEditForm(request.POST,request.FILES, instance=edit_prod)
        if update_form.is_valid():
            update_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[edit_prod.category_id]))
    else:
        update_form = ProductEditForm(instance=edit_prod)

    content = {
        'form':update_form ,
        'category':edit_prod.category
    }

    return render(request, 'adminapp/product_update.html', content)

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admin:category_read')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование категории'
        context['name_category'] = self.get_object()
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'


    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        category_pk = self.object.category.id
        context = super().get_context_data(**kwargs)
        context['category'] = category_pk
        return context

    def get_success_url(self):
        category_pk = self.object.category.id
        return reverse_lazy('adminapp:products', args=[category_pk])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())