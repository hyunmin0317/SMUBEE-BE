from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    major = models.CharField(max_length=20)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username
