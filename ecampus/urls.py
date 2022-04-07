from django.urls import path
from ecampus import views

urlpatterns = [
    path('', views.home),
]
