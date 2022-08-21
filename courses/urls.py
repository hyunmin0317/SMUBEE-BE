from django.urls import path
from courses.views import CourseAPI, AssignAPI, SubjectListAPI

urlpatterns = [
    path('all/', SubjectListAPI.as_view()),
    path('<str:code>/course/', CourseAPI.as_view()),
    path('<str:code>/assign/', AssignAPI.as_view()),
]