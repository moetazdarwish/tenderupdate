from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('addCartItem', views.addCartItem, name="addCartItem"),
    path('cartdetails', views.cartDetails, name="cartDetails"),
    path('login', views.userlogin, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('adminPage', views.adminPage, name="adminPage"),
    ]