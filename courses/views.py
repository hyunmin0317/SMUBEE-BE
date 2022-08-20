from rest_framework.generics import ListAPIView
from planners.models import Plan
from planners.serializers import PlanSerializer


class CourseAPI(ListAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return Plan.objects.filter(user=self.request.user, code=code, category='course')


class AssignAPI(ListAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return Plan.objects.filter(user=self.request.user, code=code, category='assign')