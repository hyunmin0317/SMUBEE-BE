from django.urls import path
from .views import AnnounceListAPI, update

urlpatterns = [
    path('all/', AnnounceListAPI.as_view()),
    path('update/', update),
]