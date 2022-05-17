from django.db import models


class Announcement(models.Model):

    CATEGORY_SEO = "Seoul"
    CATEGORY_CHEO = "Cheonan"

    CATEGORY_CHOICES = (
        (CATEGORY_SEO, "seoul"),
        (CATEGORY_CHEO, "cheonan"),
    )

    title = models.CharField(max_length=30)
    pinned = models.BooleanField(default=False)
    created = models.DateField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    view_count = models.IntegerField()
    more_link = models.CharField(max_length=200)
