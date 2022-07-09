import json
from datetime import datetime
from crawling import course_data
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from planners.models import Plan
from planners.serializers import PlanSerializer, CreateSerializer
from users.models import Profile


class PlanListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user)


class ClassListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user, category='Class')


class DetailAPI(RetrieveAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class UpdateAPI(UpdateAPIView):
    queryset = Plan.objects.all()
    serializer_class = CreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteAPI(DestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class DateAPI(ListAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        date = self.kwargs['date']
        q = Q()
        q &= Q(user=self.request.user)
        q &= Q(date__range=[date+' 00:00:00', date+' 23:59:59'])
        return Plan.objects.filter(q)


class CreateAPI(CreateAPIView):
    serializer_class = CreateSerializer
    def perform_create(self, serializer):
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        serializer.save(user=self.request.user, category='Plan', date=date)


def course_update(id, password, user):
    data_list = course_data(id, password)
    for data in data_list:
        updated_rows = Plan.objects.filter(user_id=user.id, title=data['title'], category='Class').update(content=data['content'])
        if not updated_rows:
            Plan.objects.create(user_id=user.id, title=data['title'], category='Class', content=data['content'], date=data['date'])


def update(request):
    user = request.user
    id = user.username
    password = Profile.objects.get(user=user).password
    try:
        course_update(id, password, user)
        return HttpResponse(json.dumps({'response': 'success'}))
    except:
        return HttpResponse(json.dumps({'response': 'fail'}))
