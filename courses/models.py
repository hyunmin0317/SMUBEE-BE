from django.db import models
from django.contrib.auth.models import User
from professors import models as professor_models


class Course(models.Model):
    title = models.CharField(max_length=20)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    professor = models.ForeignKey(
        professor_models.Professor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
    )
