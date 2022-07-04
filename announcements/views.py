import json
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from announcements.models import Announcement
from announcements.serializers import AnnounceSerializer
from crawling import announce_update


class AnnounceListAPI(ListAPIView):
    queryset = Announcement.objects.all().order_by('-number')
    serializer_class = AnnounceSerializer


class AnnounceFilterAPI(ListAPIView):
    serializer_class = AnnounceSerializer

    def get_queryset(self):
        campus = self.kwargs['campus']
        queryset = Announcement.objects.filter(Q(campus='both')|Q(campus=campus)).order_by('-number')
        return queryset


def update(request):
    try:
        announce_update()
        return HttpResponse(json.dumps({'response': 'success'}))
    except:
        return HttpResponse(json.dumps({'response': 'fail'}))