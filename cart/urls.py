from django.urls import path, include
from . import views

urlpatterns = [
    path('createCart/', views.createCart, name="createCart"),
    path('posLogin/', views.posLogin, name="posLogin"),
    path('postasklogin/', views.posTaskLogin, name="posTaskLogin"),
    path('posCash/<pk>/', views.posCash, name="posCash"),
    path('posclose/<pk>/', views.posClose, name="posClose"),
    path('posPage/<pk>/', views.posPage, name="posPage"),
    path('cartsubtotal/<pk>/', views.cartSubTotal, name="cartSubTotal"),
    path('paymnt/<pk>/', views.paymnt, name="paymnt"),
    path('task/<pk>/', views.taskPOS, name="taskPOS"),
    path('invpos/<pk>/', views.invPOS, name="invPOS"),
    path('posMode/<pk>/', views.posMode, name="posMode"),
    path('cartbusiness/<pk>/', views.cartbusiness, name="cartbusiness"),
    path('custmerorders/<pk>/', views.custmerOrders, name="custmerOrders"),
    path('checkDiscount/<pk>/', views.checkDiscount, name="checkDiscount"),
    path('checkDelivery/<pk>/', views.checkDelivery, name="checkDelivery"),
    path('businesprint/<pk>/', views.businesPrint, name="businesPrint"),
    path('cartprint/<pk>/', views.cartPrint, name="cartPrint"),

    # cust
    path('cartcustomer/', views.cartCustomer, name="cartCustomer"),
    path('cartaccount/', views.cartAccount, name="cartAccount"),
    path('posbackUp/', views.posbackUp, name="posbackUp"),


    ]