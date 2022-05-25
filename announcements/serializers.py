from rest_framework import serializers
from announcements.models import Announcement

class AnnounceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'