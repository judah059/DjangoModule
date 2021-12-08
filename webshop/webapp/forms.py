from django import forms
import datetime
from django.forms import ModelForm
from .models import Purchase, Product, MyUser, Return


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


# class AddReturnForm(ModelForm):
#     class Meta:
#         model = Return
#
#     def clean(self):
#         cleaned_data = super().clean()
#         purchase = cleaned_data.get('purchase')
#         diff = datetime.datetime.now() - purchase.created_at
#         if diff.total_seconds() > 180:
#             self.add_error('purchase', 'Sorry, you can`t return this product')


class AddPurchaseForm(ModelForm):

    class Meta:
        model = Purchase
        fields = ['product', 'purchase_product_count']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     purchase_product_count = cleaned_data.get('purchase_product_count')
    #     product = cleaned_data.get('product')
    #     # sum_ = product.price * purchase_product_count
    #     # my_user = cleaned_data.get('user')
    #     # if sum_ > my_user.wallet:
    #     #     self.add_error('product_count', 'You don`t have enough money')
    #     if product.product_count == 0:
    #         self.add_error('product_count', 'Sorry product is over')
    #     if purchase_product_count > product.product_count:
    #         self.add_error('product_count', 'Not enough products')



