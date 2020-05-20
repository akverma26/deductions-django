from django.urls import path

from . import views

urlpatterns = [
    path('make_databse', views.make_databse, name='make_databse'),
]