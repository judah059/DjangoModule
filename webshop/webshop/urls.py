from django.contrib import admin
from django.urls import path
from webapp.views import Login, Register, AddProductView, ProductView, DetailProductView, UpdateProductView, ReturnView, Logout, PurchaseView, PurchaseDelete, ReturnDelete
from rest_framework.authtoken import views

from webapp.API.resources import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('purchase/delete/<int:pk>/', PurchaseDelete.as_view(), name='purchase-delete'),
    path('', ProductView.as_view(), name='main'),
    path('logout/', Logout.as_view(), name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('product/create/', AddProductView.as_view(), name='add-product'),
    path('<int:pk>/', DetailProductView.as_view(), name='detail-product'),
    path('update/<int:pk>/', UpdateProductView.as_view(), name='update-product'),
    path('return/', ReturnView.as_view(), name='return'),
    path('purchase/list/', PurchaseView.as_view(), name='purchase'),
    path('return/delete/<int:pk>/', ReturnDelete.as_view(), name='return-delete'),
    path('api-token-auth/', CustomAuthToken.as_view())


]
