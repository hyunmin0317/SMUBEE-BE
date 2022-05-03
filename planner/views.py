from datetime import datetime
from .crawling import course_data
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from planner.models import Plan
from planner.serializers import PlanSerializer, CreateSerializer
from user.models import Profile


class ListAPI(ListAPIView):
    serializer_class = PlanSerializer
    def get_queryset(self):
        user = self.request.user
        id = user.username
        password = Profile.objects.get(user=user).password
        update(id, password, user)
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
        q = Q()
        q &= Q(user=self.request.user)
        q &= Q(date__range=[date+'+00:00:00', date+'+23:59:59'])
        return Plan.objects.filter(q)

class CreateAPI(CreateAPIView):
    serializer_class = CreateSerializer
    def perform_create(self, serializer):
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        serializer.save(user=self.request.user, date=date)


def update(id, password, user):
    data_list = course_data(id, password)
    for data in data_list:
        content = '수업명: '+data['course']+'\n진도율: '+data['ratio']
        date = data['close'][:10]
        updated_rows = Plan.objects.filter(user_id=user.id, title=data['name']).update(content=content)
        if not updated_rows:
            Plan.objects.create(user_id=user.id, title=data['name'], content=content, date=date)
#
# def login(id, password):
#     user_info = {'username': id, 'password': password}
#     session = requests.Session()
#     request = session.post('https://ecampus.smu.ac.kr/login/index.php', data=user_info)
#
#     # 로그인 성공
#     if request.url == 'https://ecampus.smu.ac.kr/':
#         return session
#     return -1
#
# def subject(session):
#     data = []
#     request = session.get('https://ecampus.smu.ac.kr/')
#     source = request.text
#     soup = bs(source, 'html.parser')
#
#     code_list = soup.select('#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a')
#
#     for code in code_list:
#         data.append(code['href'].split('=')[1])
#     return data
#
#
#
#
#
# def course(session, code, user_id):
#     ratios = []
#     request = session.get('https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id='+code)
#     source = request.text
#     soup = bs(source, 'html.parser')
#     body = soup.find("table", class_="user_progress")
#
#     if body is not None:
#         names = body.find_all("td", class_="text-left")
#         closes = body.find_all('button', class_='track_detail')
#
#         i = 0
#         courses = body.find_all('td', class_='text-center')
#         for course in courses:
#             if course['class'][0] == 'text-center':
#                 i += 1
#                 if i % 3 == 0:
#                     ratios.append(course.text)
#
#         for name, ratio, close in zip(names, ratios, closes):
#             updated_rows = Plan.objects.filter(user_id=user_id, title=name.text).update(content=ratio)
#             if not updated_rows:
#                 # if not exists, create new
#                 Plan.objects.create(user_id=user_id, title=name.text, content=ratio, date=close['title'].split('~')[1][1:-1])