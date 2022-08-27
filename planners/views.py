from datetime import datetime
from courses.models import Subject
from crawling import course_data
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from planners.models import Plan
from planners.serializers import PlanSerializer, CreateSerializer
from users.models import Profile


class PlanListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user, category='plan')


class ClassListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        queryset = Plan.objects.filter(Q(user=self.request.user)&(Q(category="course")|Q(category="assign"))).order_by('-date')
        return queryset

class ClassCheckListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        status = self.kwargs['status']
        checked = (status == "complete")
        queryset = Plan.objects.filter(Q(user=self.request.user)&(Q(category="course")|Q(category="assign"))&Q(checked=checked)).order_by('-date')
        return queryset

class CourseListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user, category='course')


class AssignListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        return Plan.objects.filter(user=self.request.user, category='assign')


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
        serializer.save(user=self.request.user, category='plan', date=date)


def course_update(id, password, user):
    data_list, subjects = course_data(id, password)
    for data in data_list:
        checked = False
        if data['category'] == 'course':
            if data['status'] == '100%':
                checked = True
        else:
            if data['status'] == '제출 완료':
                checked = True

        updated_rows = Plan.objects.filter(user_id=user.id, course=data['name'], title=data['title'], category=data['category'], code=data['code']).update(content=data['content'], status=data['status'], checked=checked)
        if not updated_rows:
            try:
                Plan.objects.create(user_id=user.id, course=data['name'], title=data['title'], category=data['category'], content=data['content'], date=data['date'], status=data['status'], checked=checked, code=data['code'])
            except:
                continue

        for sub in subjects:
            updated_rows = Subject.objects.filter(user_id=user.id, name=sub["name"], prof=sub["prof"], code=sub["code"])
            if not updated_rows:
                Subject.objects.create(user_id=user.id, name=sub["name"], prof=sub["prof"], code=sub["code"])


class update(ListAPIView):
    serializer_class = PlanSerializer

    def get_queryset(self):
        user = self.request.user
        id = user.username
        password = Profile.objects.get(user=user).password
        course_update(id, password, user)
        queryset = Plan.objects.filter(user=self.request.user, category='course')
        queryset.union(Plan.objects.filter(user=self.request.user, category='assign'))
        return queryset
