from django.contrib import admin
from . import models


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    ordering = [
        "-number",
    ]
