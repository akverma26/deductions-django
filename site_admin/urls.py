from django.urls import path

from . import views

urlpatterns = [
    path('', views.add_deduction, name='add-deduction'),
    path('add-deduction/', views.add_deduction, name='add-deduction'),
    path('refresh-files/', views.refresh_files, name='refresh-files'),
    path('track-server/', views.track_server, name='track-server'),
]