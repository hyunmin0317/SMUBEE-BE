from django.urls import path
from courses.views import CourseAPI, AssignAPI, SubjectListAPI, check

urlpatterns = [
    path('all/', SubjectListAPI.as_view()),
    path('check/', check),
    path('<str:code>/course/', CourseAPI.as_view()),
    path('<str:code>/assign/', AssignAPI.as_view()),
]