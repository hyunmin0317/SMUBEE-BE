from rest_framework.generics import ListAPIView
from announcements.models import Announcement
from announcements.serializers import AnnounceSerializer


class AnnounceListAPI(ListAPIView):
    queryset = Announcement.objects.all().order_by('-number')
    serializer_class = AnnounceSerializer