from django.urls import path, include
from . import views

urlpatterns = [
    path('ingredient/', views.ingredient, name="ingredient"),
    path('task/', views.task_kitchen, name="kitchenTask"),
    # recipt
    path('kitCategory/', views.kitCategory, name="kitCategory"),
    path('reciptls/', views.reciptls, name="reciptls"),
    path('task_Recipe/', views.task_Recipe, name="task_Recipe"),
    # pricing
    path('pricing/', views.pricing, name="pricing"),
    path('btn_price/', views.btn_price, name="btn_price"),
    # task
    path('lsttask/', views.task, name="task"),
    path('kitbackUp/', views.kitbackUp, name="kitbackUp"),
    # task

    ]