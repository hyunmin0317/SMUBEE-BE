import json
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from announcements.models import Announcement
from announcements.serializers import AnnounceSerializer
from crawling import announce_update


class AnnounceListAPI(ListAPIView):
    queryset = Announcement.objects.all().order_by('-number')
    serializer_class = AnnounceSerializer


def update(request):
    try:
        announce_update()
        return HttpResponse(json.dumps({'response': 'success'}))
    except:
        return HttpResponse(json.dumps({'response': 'fail'}))