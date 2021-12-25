import mimetypes

from django.db import transaction
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import FormMixin, DeleteView
from .forms import AddProductForm, AddPurchaseForm, MyUserCreationForm, AddReturnForm
from .models import Product, Return, MyUser, Purchase
from django.contrib import messages


class Login(LoginView):
    template_name = 'login.html'

    # def get_success_url(self):
    #     return HttpResponseRedirect('/')


class Register(CreateView):
    form_class = MyUserCreationForm
    template_name = 'register.html'
    success_url = '/login/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = '/login/'


class AddProductView(CreateView):
    form_class = AddProductForm
    template_name = 'addProduct.html'
    success_url = '/'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        if not self.request.user.is_superuser:
            raise Http404
        return form_class(**self.get_form_kwargs())


class ProductView(ListView):
    model = Product
    template_name = 'main.html'
    paginate_by = 15
    login_url = 'login/'


class DetailProductView(FormMixin, DetailView):
    model = Product
    template_name = 'product.html'
    pk_url_kwarg = 'pk'
    form_class = AddPurchaseForm

    def get_success_url(self):
        return reverse('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kw = super(DetailProductView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        product_id = self.request.POST.get('product')
        obj.product = Product.objects.get(id=product_id)
        obj.product.product_count = obj.product.product_count - obj.purchase_product_count
        sum_ = obj.product.price * obj.purchase_product_count
        obj.user.wallet = obj.user.wallet - sum_
        obj.product.save()
        obj.user.save()
        obj.save()
        return super().form_valid(form=form)


class UpdateProductView(UpdateView):
    model = Product
    fields = ['name', 'producer', 'description', 'price', 'product_count']
    template_name = 'update.html'
    success_url = '/'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        if not self.request.user.is_superuser:
            raise Http404
        return form_class(**self.get_form_kwargs())


class ReturnView(ListView):
    model = Return
    template_name = 'return.html'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs.all()
        else:
            return qs.filter(purchase__user=self.request.user)


class PurchaseView(FormMixin, ListView):
    model = Purchase
    template_name = 'purchase.html'
    paginate_by = 15
    form_class = AddReturnForm

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs.all()
        else:
            return qs.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kw = super(PurchaseView, self).get_form_kwargs()
        kw['request'] = self.request
        return kw

    def form_valid(self, form):
        obj = form.save(commit=False)
        purchase_id = self.request.POST.get('purchase')
        obj.purchase = Purchase.objects.get(id=purchase_id)
        obj.save()
        return super().form_valid(form=form)


class PurchaseDelete(DeleteView):
    model = Purchase
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        product = self.object.product
        product.product_count = product.product_count + self.object.purchase_product_count
        user = self.object.user
        user.wallet += self.object.purchase_product_count * product.price
        with transaction.atomic():
            product.save()
            user.save()
            self.object.delete()
        return HttpResponseRedirect(success_url)


class ReturnDelete(DeleteView):
    model = Return
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)




# Create your views here.
