from django.urls import path
from .views import AnnounceListAPI, AnnounceFilterAPI, update

urlpatterns = [
    path('all/', AnnounceListAPI.as_view()),
    path('<str:campus>/', AnnounceFilterAPI.as_view()),
    path('update/', update),
]