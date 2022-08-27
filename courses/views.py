from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from courses.models import Subject
from courses.serializers import SubjectSerializer
from crawling import login, subject
from planners.models import Plan
from planners.serializers import PlanSerializer
from users.models import Profile


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


class update(ListAPIView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        user = self.request.user
        id = user.username
        password = Profile.objects.get(user=user).password
        session = login(id, password)
        subjects = subject(session)
        for sub in subjects:
            updated_rows = Subject.objects.filter(user_id=user.id, name=sub["name"], prof=sub["prof"], code=sub["code"])
            if not updated_rows:
                Subject.objects.create(user_id=user.id, name=sub["name"], prof=sub["prof"], code=sub["code"])
        return Subject.objects.filter(user=self.request.user)

@api_view(['GET'])
def check(request):
    complete = Plan.objects.filter(Q(user=request.user) & (Q(category="course") | Q(category="assign")) & Q(checked=True)).count()
    incomplete = Plan.objects.filter(Q(user=request.user) & (Q(category="course") | Q(category="assign")) & Q(checked=False)).count()
    res = {'complete': complete, 'incomplete': incomplete}
    return Response(res, status=status.HTTP_200_OK)
