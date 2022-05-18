from django.db import models
from core import models as core_models


class Notification(core_models.TimeStampedModel):

    content = models.TextField(max_length=200)
    erased = models.BooleanField(default=False)
    link = models.URLField(max_length=200)

    