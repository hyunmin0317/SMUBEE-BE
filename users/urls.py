# api/urls.py
from django.urls import path
from .views import LoginAPI, UserAPI

urlpatterns = [
    path("login/", LoginAPI.as_view()),
    path("users/", UserAPI.as_view()),
]