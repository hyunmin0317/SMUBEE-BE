from django.db import models
from users import models as user_models
from professors import models as professor_models


class Course(models.Model):
    title = models.CharField(max_length=20)
    course_code = models.CharField(max_length=10)  # 학수번호
    class_number = models.IntegerField()  # 분반
    course_id = models.IntegerField(null=True)  # 크롤링을 위한 URL id

    student = models.ManyToManyField(
        user_models.Profile,
        related_name="courses",
        on_delete=models.SET_NULL,
        blank=True,
    )
    professor = models.ManyToManyField(
        professor_models.Professor,
        related_name="courses",
        on_delete=models.SET_NULL,
        blank=True,
    )

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.week


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
