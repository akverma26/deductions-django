from django.urls import path

from . import views

urlpatterns = [
    path('', views.add_deduction, name='add-deduction'),
    path('add-deduction/', views.add_deduction, name='add-deduction'),
]