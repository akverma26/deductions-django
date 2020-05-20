from django.urls import path

from . import views

urlpatterns = [
    path('post/<str:post_id>', views.post, name='post'),
]