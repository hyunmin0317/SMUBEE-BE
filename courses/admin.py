from django.contrib import admin
from . import models

admin.site.register(models.Course)
admin.site.register(models.Week)
admin.site.register(models.LectureVideo)
admin.site.register(models.Assignment)
