from django.contrib import admin
from django.urls import path
from webapp.views import Login, Register, AddProductView, ProductView, DetailProductView, UpdateProductView, ReturnView, AddReturnView, AddPurchaseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductView.as_view(), name='main'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('product/create/', AddProductView.as_view(), name='add-product'),
    path('<int:pk>/', DetailProductView.as_view(), name='detail-product'),
    path('update/<int:pk>/', UpdateProductView.as_view(), name='update-product'),
    path('return/', ReturnView.as_view(), name='return'),
    path('purchase/<int:pk>/', AddReturnView.as_view(), name='add-return'),
    path('purchase/', AddPurchaseView.as_view(), name='add-purchase')

]
