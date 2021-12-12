from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=1000)


class Product(models.Model):
    name = models.CharField(max_length=120)
    producer = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=12)
    product_count = models.IntegerField()


class Purchase(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    purchase_product_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)



class Return(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='returns')
    reason = models.CharField(max_length=120, null=True, blank=True)
    request_time = models.TimeField(auto_now=True)


# Create your models here.
