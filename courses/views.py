from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from courses.models import Subject
from courses.serializers import SubjectSerializer
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


class SubjectListAPI(ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)


@api_view(['GET'])
def check(request):
    complete = Plan.objects.filter(Q(user=request.user) & (Q(category="course") | Q(category="assign")) & Q(checked=True)).count()
    incomplete = Plan.objects.filter(Q(user=request.user) & (Q(category="course") | Q(category="assign")) & Q(checked=False)).count()
    res = {'complete': complete, 'incomplete': incomplete}
    return Response(res, status=status.HTTP_200_OK)
