from django import forms
import datetime
from django.forms import ModelForm
from .models import Purchase, Product, MyUser, Return
from django.contrib.auth.forms import UserCreationForm


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'producer', 'description', 'price', 'product_count']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        producer = cleaned_data.get('producer')
        product_count = cleaned_data.get('product_count')
        if price <= 0:
            self.add_error('price', 'Prise has to be greater than zero')
        if product_count <= 0:
            self.add_error('product_count', 'You can not add a product, if you haven`t one')
        if name and price and producer in Product.objects.all():
            self.add_error('name', 'This product already has added')


class AddReturnForm(ModelForm):
    class Meta:
        model = Return
        fields = ['reason']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddReturnForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        purchase_id = self.request.POST.get('purchase')
        purchase = Purchase.objects.get(id=purchase_id)
        duration = datetime.datetime.now(datetime.timezone.utc) - purchase.created_at
        if Return.objects.filter(purchase=purchase):
            self.add_error(None, 'You has already tried to return')
        elif duration.total_seconds() > 180:
            self.add_error(None, 'Time for return is over. You could return in 180 seconds')


class AddPurchaseForm(ModelForm):

    class Meta:
        model = Purchase
        fields = ['purchase_product_count']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddPurchaseForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        purchase_product_count = cleaned_data.get('purchase_product_count')
        product_id = self.request.POST.get('product')
        product = Product.objects.get(id=product_id)
        sum_ = product.price * purchase_product_count
        my_user = self.request.user
        if sum_ > my_user.wallet:
            self.add_error('purchase_product_count', 'You don`t have enough money')
        if purchase_product_count > product.product_count:
            self.add_error('purchase_product_count', 'Not enough products')
        elif purchase_product_count <= 0:
            self.add_error('purchase_product_count', 'Please select one or more products')


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username",)

