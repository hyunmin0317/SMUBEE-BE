from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=20)
    major = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username
