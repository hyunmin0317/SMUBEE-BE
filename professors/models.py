from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=20)
    office = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=30)
    contact_number = models.CharField(max_length=20, null=True)
    more_link = models.CharField(max_length=300)

    def __str__(self):
        return self.name
