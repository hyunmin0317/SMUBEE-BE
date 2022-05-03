from django.contrib.auth.models import User
from django.db import models


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title