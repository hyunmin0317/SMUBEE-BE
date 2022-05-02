from datetime import datetime
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from planner.models import Plan
from planner.serializers import PlanSerializer, CreateSerializer


class ListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user)

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
        print(date)
        q = Q()
        q &= Q(user=self.request.user)
        q &= Q(date__range=[date+'+00:00:00', date+'+23:59:59'])
        return Plan.objects.filter(q)

class CreateAPI(CreateAPIView):
    serializer_class = CreateSerializer
    def perform_create(self, serializer):
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        serializer.save(user=self.request.user, date=date)