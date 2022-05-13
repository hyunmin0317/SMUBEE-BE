import requests
from bs4 import BeautifulSoup as bs
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from users.models import Profile


def login(id, password):
    user_info = {'username': id, 'password': password}
    session = requests.Session()
    request = session.post('https://ecampus.smu.ac.kr/login/index.php', data=user_info)

    # 로그인 성공
    if request.url == 'https://ecampus.smu.ac.kr/':
        return session
    return -1


def course(session, code):
    data = []
    names = []
    ratios = []
    closes = []

    request = session.get('https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id='+code)
    source = request.text
    soup = bs(source, 'html.parser')

    body = soup.find("table", class_="user_progress")

    if body is None:
        return data

    courses = body.find_all("td", class_="text-left")
    for course in courses:
        names.append(course.text)

    i = 0
    courses = body.find_all('td', class_='text-center')
    for course in courses:
        if course['class'][0] == 'text-center':
            i += 1
            if i % 3 == 0:
                ratios.append(course.text)

    courses = body.find_all('button', class_='track_detail')
    for course in courses:
        closes.append(course['title'].split('~')[1][1:-1])

    for name, ratio, close in zip(names, ratios, closes):
        data.append({'name': name, 'ratio': ratio, 'close': close})
    return data


def subject(session):
    data = []
    request = session.get('https://ecampus.smu.ac.kr/')
    source = request.text
    soup = bs(source, 'html.parser')


    name_list = soup.select('#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a > div.course-name > div.course-title > h3')
    prof_list = soup.select('#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a > div.course-name > div.course-title > p')
    code_list = soup.select('#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a')

    for name, prof, code in zip(name_list, prof_list, code_list):
        dic = {'name': name.text, 'prof': prof.text, 'code': code['href'].split('=')[1]}
        data.append(dic)
    return data


def assign(session, code):
    data = []
    request = session.get('https://ecampus.smu.ac.kr/mod/assign/index.php?id='+code)
    source = request.text
    soup = bs(source, 'html.parser')

    names = soup.find_all('td', class_='cell c1')
    closes = soup.find_all('td', class_='cell c2')
    submits = soup.find_all('td', class_='cell c3')
    subject_name = soup.select('#page-header > nav > div > div.coursename > h1 > a')[0].text

    for name, close, submit in zip(names, closes, submits):
        data.append({'name': name.text, 'close': close.text, 'submit': submit.text})
    return data, subject_name


@login_required(login_url='users:login')
def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        try:
            profile = Profile.objects.get(user_id=user.id)
        except:
            Profile.objects.create(user=user)

    id = request.user.username
    password = profile.password
    session = login(id, password)

    if session == -1:
        context = {'error': -1}
    else:
        subjects = subject(session)
        context = {'subjects': subjects}
    return render(request, 'ecampus/home.html', context)


@login_required(login_url='users:login')
def detail(request, code):
    user = request.user
    id = user.username
    password = Profile.objects.get(user=user).password
    session = login(id, password)

    assigns, name = assign(session, code)
    courses = course(session, code)

    if session == -1:
        print('로그인 실패')
    else:
        context = {'name': name, 'assigns': assigns, 'courses': courses}
    return render(request, 'ecampus/detail.html', context)


@login_required(login_url='users:login')
def all(request):
    courses = []
    assigns = []
    user = request.user
    id = user.username
    password = Profile.objects.get(user=user).password
    session = login(id, password)

    if session == -1:
        print('로그인 실패')
    else:
        subjects = subject(session)
        for s in subjects:
            courses += course(session, s['code'])
            ass, name = assign(session, s['code'])
            assigns += ass
    context = {'courses': courses, 'assigns': assigns}
    return render(request, 'ecampus/detail.html', context)

@login_required(login_url='users:login')
def calendar(request):
    context = {'email':request.user.email}
    return render(request, 'ecampus/calendar.html', context)