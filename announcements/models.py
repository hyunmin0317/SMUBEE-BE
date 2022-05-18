from django.db import models


class Announcement(models.Model):

    CAMPUS_SEO = "seoul"
    CAMPUS_CHEO = "cheonan"
    CAMPUS_BOTH = "both"

    CAMPUS_CHOICES = (
        (CAMPUS_SEO, "Seoul"),
        (CAMPUS_CHEO, "Cheonan"),
        (CAMPUS_BOTH, "Both"),
    )

    title = models.CharField(max_length=30)
    pinned = models.BooleanField(default=False)
    number = models.IntegerField(unique=True, primary_key=True)
    created_date = models.DateField()
    campus = models.CharField(max_length=10, choices=CAMPUS_CHOICES)
    views = models.IntegerField()
    more_link = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.number} :: {self.created_date}"
