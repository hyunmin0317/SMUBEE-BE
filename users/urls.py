# api/urls.py
from django.urls import path
from .views import RegistrationAPI, LoginAPI, UserAPI

urlpatterns = [
    path("signup/", RegistrationAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("users/", UserAPI.as_view()),
]