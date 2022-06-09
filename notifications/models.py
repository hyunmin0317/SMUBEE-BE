from django.db import models
from core import models as core_models
from users import models as user_models


class Notification(core_models.TimeStampedModel):

    category = models.CharField(max_length=10)
    content = models.TextField(max_length=200)
    erased = models.BooleanField(default=False)
    link = models.URLField(max_length=200)

    user = models.ForeignKey(
        user_models.Profile, on_delete=models.CASCADE, related_name="notifications"
    )
