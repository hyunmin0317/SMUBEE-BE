from django.urls import path
from ecampus import views

app_name = 'ecampus'

urlpatterns = [
    path('all/', views.all, name='all'),
    path('<str:code>/', views.detail, name='detail'),
]
