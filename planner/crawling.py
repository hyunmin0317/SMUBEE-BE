import requests
from bs4 import BeautifulSoup as bs


def login(id, password):
    user_info = {'username': id, 'password': password}
    session = requests.Session()
    request = session.post('https://ecampus.smu.ac.kr/login/index.php', data=user_info)

    # 로그인 성공
    if request.url == 'https://ecampus.smu.ac.kr/':
        return session
    return -1


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


def course(session, course_name, code):
    data = []
    ratios = []
    request = session.get('https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id='+code)
    source = request.text
    soup = bs(source, 'html.parser')
    body = soup.find("table", class_="user_progress")

    if body is None:
        return data

    names = body.find_all("td", class_="text-left")
    closes = body.find_all('button', class_='track_detail')

    i = 0
    courses = body.find_all('td', class_='text-center')
    for course in courses:
        if course['class'][0] == 'text-center':
            i += 1
            if i % 3 == 0:
                ratios.append(course.text)

    for name, ratio, close in zip(names, ratios, closes):
        title = f'강의-{name.text}'
        content = f'수업명: {course_name}\n현황: {ratio}'
        data.append({'title': title, 'content': content, 'date': close['title'].split('~')[1][1:-1][:10]})
    return data


def assign(session, course_name, code):
    data = []
    request = session.get('https://ecampus.smu.ac.kr/mod/assign/index.php?id='+code)
    source = request.text
    soup = bs(source, 'html.parser')

    names = soup.find_all('td', class_='cell c1')
    closes = soup.find_all('td', class_='cell c2')
    submits = soup.find_all('td', class_='cell c3')

    for name, close, submit in zip(names, closes, submits):
        title = f'과제-{name.text}'
        content = f'수업명: {course_name}\n현황: {submit.text}'
        data.append({'title': title, 'content': content, 'date': close.text[:10]})
    return data


def course_data(id, password):
    data = []
    session = login(id, password)

    if session == -1:
        print('로그인 실패')
    else:
        subjects = subject(session)
        for sub in subjects:
            data += course(session, sub['name'], sub['code'])
            data += assign(session, sub['name'], sub['code'])
    return data