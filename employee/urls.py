from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.create_Employee, name="create_Employee"),
    path('list/', views.list_Employee, name="list_Employee"),
    path('salary/', views.salary_employee, name="salary_employee"),
    path('ticket/', views.ticket_employee, name="ticket_employee"),
    path('lst_ticket/', views.ticket_List, name="ticket_List"),
    path('attendence/', views.attendence_employee, name="attendence_employee"),
    path('genr_attendence/', views.user_attendence, name="user_attendence"),
    path('attend/', views.attendenceList, name="attendenceList"),
    path('createadvance/', views.createAdvance, name="createAdvance"),
    ]