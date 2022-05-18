from django.db import models
from django.contrib.auth.models import User
from professors import models as professor_models


class Course(models.Model):
    title = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    professor = models.ForeignKey(
        professor_models.Professor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
    )


class Week(models.Model):
    week = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="weeks")


class LectureVideo(models.Model):
    title = models.CharField(max_length=100)
    progress = models.IntegerField()
    finished = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="lectures")

    def __str__(self):
        return f"{self.week} :: {self.title}"


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="assignments")

    def __str__(self):
        return f"{self.week} :: {self.title}"
