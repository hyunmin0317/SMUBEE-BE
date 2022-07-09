# api/urls.py
from django.urls import path
from .views import CreateAPI, PlanListAPI, ClassListAPI, DetailAPI, DeleteAPI, UpdateAPI, DateAPI, update

urlpatterns = [
    path('plan/all/', PlanListAPI.as_view()),
    path('class/all/', ClassListAPI.as_view()),
    path('date/<str:date>/', DateAPI.as_view()),
    path('date/<str:date>/create/', CreateAPI.as_view()),
    path('update/', update),
    path('<int:pk>/', DetailAPI.as_view()),
    path('<int:pk>/update/', UpdateAPI.as_view()),
    path('<int:pk>/delete/', DeleteAPI.as_view()),
]