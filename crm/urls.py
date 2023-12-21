from django.urls import path, include
from . import views

urlpatterns = [
    path('customerList/', views.customerList, name="customerList"),
    path('customerAdd/', views.customerAdd, name="customerAdd"),
    path('discount/', views.createDiscount, name="createDiscount"),
    path('crmbackUp/', views.crmbackUp, name="crmbackUp"),

    ]