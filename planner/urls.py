# api/urls.py
from django.urls import path
from .views import CreateAPI, ListAPI, DetailAPI, DeleteAPI, UpdateAPI, DateAPI

urlpatterns = [
    path('all/', ListAPI.as_view()),
    path('create/', CreateAPI.as_view()),
    path('date/<str:date>/', DateAPI.as_view()),
    path('<int:pk>/', DetailAPI.as_view()),
    path('<int:pk>/update/', UpdateAPI.as_view()),
    path('<int:pk>/delete/', DeleteAPI.as_view()),
]