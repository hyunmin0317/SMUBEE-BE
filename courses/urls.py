from django.urls import path
from courses.views import CourseAPI, AssignAPI, SubjectListAPI, CheckAPI, check, update

urlpatterns = [
    path('all/', SubjectListAPI.as_view()),
    path('update/', update.as_view()),
    path('check/', check),
    path('check/<int:checked>/', CheckAPI.as_view()),
    path('<str:code>/course/', CourseAPI.as_view()),
    path('<str:code>/assign/', AssignAPI.as_view()),
]