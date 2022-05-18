from django.contrib import admin
from . import models


@admin.register(models.Professor)
class ProfessorAdmin(admin.ModelAdmin):

    ordering = [
        "name",
    ]
