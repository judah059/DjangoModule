from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .forms import AddProductForm, AddPurchaseForm
from .models import Product, Return


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'


class Register(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = '/'


class Logout(LogoutView):
    next_page = '/'
    login_url = 'login/'


class AddProductView(CreateView):
    form_class = AddProductForm
    template_name = 'addProduct.html'
    success_url = '/'


class ProductView(ListView):
    model = Product
    template_name = 'main.html'
    paginate_by = 15


class DetailProductView(DetailView):
    model = Product
    template_name = 'product.html'
    pk_url_kwarg = 'pk'


class UpdateProductView(UpdateView):
    model = Product
    fields = ['name', 'producer', 'description', 'price', 'product_count']
    template_name = 'update.html'
    success_url = '/'


class ReturnView(ListView):
    model = Return
    template_name = 'return.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs.all()
        else:
            return qs.filter(purchase__user=self.request.user)


class AddReturnView(CreateView):
    model = Return
    template_name = 'purchase.html'
    success_url = '/'


class AddPurchaseView(CreateView):
    form_class = AddPurchaseForm
    template_name = 'product.html'
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.product = form.product
        # obj.product.product_count = obj.product.product_count - obj.purchase_product_count
        # sum_ = obj.product.price * obj.purchase_product_count
        # obj.user.wallet = obj.user.wallet - sum_
        # obj.product.save()
        # obj.user.save()
        obj.save()


# Create your views here.
