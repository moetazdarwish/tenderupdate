from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.productCreation, name="productCreation"),
    path('category/', views.product_category, name="product_category"),
    path('supplier/', views.productSupplier, name="productSupplier"),
    path('stock/', views.inventory, name="inventory"),
    path('task/', views.inventoryTask, name="inventoryTask"),
    path('invbackUp/', views.invbackUp, name="invbackUp"),
    path('print_po/<pk>/', views.testpdf, name="PrintPO"),

    ]