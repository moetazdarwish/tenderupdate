from django.urls import path, include
from . import views

urlpatterns = [
    path('creataccount/', views.creatAccount, name="creatAccount"),
    path('journal/', views.journal, name="journal"),
    path('delete/', views.delete, name="delete"),
    path('accrequest/', views.accRequest, name="accRequest"),
    path('ledgers/', views.ledgers, name="ledgers"),
    path('invoices/', views.invoices, name="invoices"),
    path('requestprint/<pk>/', views.requestPrint, name="requestPrint"),
    path('backup/', views.backUp, name="backUp"),
    ]