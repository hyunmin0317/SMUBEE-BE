from django.db import models
from django.contrib.auth.models import User
from professors import models as professor_models


class Course(models.Model):
    title = models.CharField(max_length=20)
    code = models.CharField(max_length=10)  # 학수번호
    divided_class = models.IntegerField()  # 분반
    student = models.ManyToManyField(
        User,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
    )
    professor = models.ForeignKey(
        professor_models.Professor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses",
    )


class Week(models.Model):

    WEEK_1ST = 1
    WEEK_2ND = 2
    WEEK_3RD = 3
    WEEK_4TH = 4
    WEEK_5TH = 5
    WEEK_6TH = 6
    WEEK_7TH = 7
    WEEK_8TH = 8
    WEEK_9TH = 9
    WEEK_10TH = 10
    WEEK_11TH = 11
    WEEK_12TH = 12
    WEEK_13TH = 13
    WEEK_14TH = 14
    WEEK_15TH = 15
    WEEK_16TH = 16

    WEEK_CHOICES = (
        (WEEK_1ST, 1),
        (WEEK_2ND, 2),
        (WEEK_3RD, 3),
        (WEEK_4TH, 4),
        (WEEK_5TH, 5),
        (WEEK_6TH, 6),
        (WEEK_7TH, 7),
        (WEEK_8TH, 8),
        (WEEK_9TH, 9),
        (WEEK_10TH, 10),
        (WEEK_11TH, 11),
        (WEEK_12TH, 12),
        (WEEK_13TH, 13),
        (WEEK_14TH, 14),
        (WEEK_15TH, 15),
        (WEEK_16TH, 16),
    )

    week = models.IntegerField(choices=WEEK_CHOICES)
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
