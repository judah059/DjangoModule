from django.contrib import admin
from .models import Purchase, Product, Return, MyUser

admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Return)
admin.site.register(MyUser)

# Register your models here.
