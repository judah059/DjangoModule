from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from webapp.models import Product, MyUser, Purchase


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Purchase
        fields = '__all__'


class MyUserSerializer(serializers.ModelSerializer):
    purchases = PurchaseSerializer(many=True)
    class Meta:
        model = MyUser
        fields = ('username', 'wallet', 'purchases')

