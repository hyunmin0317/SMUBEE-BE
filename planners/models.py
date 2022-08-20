from django.contrib.auth.models import User
from django.db import models


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    content = models.TextField()
    date = models.DateTimeField()
    status = models.CharField(max_length=30)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.title