from django.urls import path
from courses.views import CourseAPI, AssignAPI

urlpatterns = [
    path('<str:code>/course/', CourseAPI.as_view()),
    path('<str:code>/assign/', AssignAPI.as_view()),
]