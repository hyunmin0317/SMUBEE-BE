from django.urls import path
from .views import AnnounceListAPI

urlpatterns = [
    path('all/', AnnounceListAPI.as_view()),
]