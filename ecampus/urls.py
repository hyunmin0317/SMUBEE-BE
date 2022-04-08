from django.urls import path
from ecampus import views

app_name = 'ecampus'

urlpatterns = [
    path('<str:code>/', views.detail, name='detail')
]
