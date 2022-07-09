import requests
from bs4 import BeautifulSoup as bs
from announcements.models import Announcement


def login(id, password):
    user_info = {"username": id, "password": password}
    session = requests.Session()
    request = session.post("https://ecampus.smu.ac.kr/login/index.php", data=user_info)

    # 로그인 성공
    if request.url == "https://ecampus.smu.ac.kr/":
        return session
    return -1


def subject(session):
    data = []
    request = session.get("https://ecampus.smu.ac.kr/")
    source = request.text
    soup = bs(source, "html.parser")

    name_list = soup.select(
        "#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a > div.course-name > div.course-title > h3"
    )
    prof_list = soup.select(
        "#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a > div.course-name > div.course-title > p"
    )
    code_list = soup.select(
        "#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a"
    )

    for names, prof, code in zip(name_list, prof_list, code_list):
        d = names.text.split("(")
        try:
            name = d[0].replace(" ", "")
            num = d[1].replace(" ", "")
            dis = d[2].split(")")[0]
            number = f"{num}-{dis}"
        except:
            continue
        dic = {
            "name": name,
            "prof": prof.text,
            "code": code["href"].split("=")[1],
            "number": number,
        }
        data.append(dic)
    return data


def course(session, course_name, code):
    data = []
    ratios = []
    request = session.get(
        "https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id=" + code
    )
    source = request.text
    soup = bs(source, "html.parser")
    body = soup.find("table", class_="user_progress")

    if body is None:
        return data

    names = body.find_all("td", class_="text-left")
    closes = body.find_all("button", class_="track_detail")

    i = 0
    courses = body.find_all("td", class_="text-center")
    for course in courses:
        if course["class"][0] == "text-center":
            i += 1
            if i % 3 == 0:
                ratios.append(course.text)

    for name, ratio, close in zip(names, ratios, closes):
        title = f"강의-{name.text}"
        content = f"수업명: {course_name}\n현황: {ratio}"
        data.append(
            {
                "title": title,
                "content": content,
                "date": close["title"].split("~")[1][1:-1][:10],
            }
        )
    return data


def assign(session, course_name, code):
    data = []
    request = session.get("https://ecampus.smu.ac.kr/mod/assign/index.php?id=" + code)
    source = request.text
    soup = bs(source, "html.parser")

    names = soup.find_all("td", class_="cell c1")
    closes = soup.find_all("td", class_="cell c2")
    submits = soup.find_all("td", class_="cell c3")

    for name, close, submit in zip(names, closes, submits):
        title = f"과제-{name.text}"
        content = f"수업명: {course_name}\n현황: {submit.text}"
        data.append({"title": title, "content": content, "date": close.text[:10]})
    return data


def course_data(id, password):
    data = []
    session = login(id, password)

    if session == -1:
        print("로그인 실패")
    else:
        subjects = subject(session)
        for sub in subjects:
            data += course(session, sub["name"], sub["code"])
            data += assign(session, sub["name"], sub["code"])
    return data


def infomation(session):
    url = "https://ecampus.smu.ac.kr/"
    request = session.get(url)
    source = request.text
    soup = bs(source, "html.parser")
    name = soup.select_one("li.user_department").text
    majar = soup.select_one("p.department").text
    return name, majar


def announce_update():
    url = "https://www.smu.ac.kr/lounge/notice/notice.do?mode=list&&articleLimit=1000&article.offset=0"
    src = requests.get(url).text
    soup = bs(src, "html.parser")
    data_list = soup.find("ul", {"class": "board-thumb-wrap"}).select("li > dl")

    for data in data_list:
        pinned = False
        content_title = data.select("dt > table > tbody > td")
        if content_title[0].find("span", {"class": "noti"}):
            pinned = True

        campus = Announcement.CAMPUS_BOTH
        campus_value = content_title[1].find("span", {"class": "cmp"})["class"]
        if "seoul" in campus_value:
            campus = Announcement.CAMPUS_SEO
        elif "cheon" in campus_value:
            campus = Announcement.CAMPUS_CHEO

        title = content_title[2].find("a").text.strip()

        content_info = data.select("dd > ul > li")
        number = int(content_info[0].text[4:].strip())
        created_date = content_info[2].text[4:].strip()
        views = int(content_info[3].text[4:].strip())
        more_link = f"https://www.smu.ac.kr/lounge/notice/notice.do?mode=view&articleNo={number}"

        try:
            announcement = Announcement.objects.get(number=number)
            announcement.update(views=views)
        except Announcement.DoesNotExist:
            Announcement.objects.create(
                title=title,
                pinned=pinned,
                number=number,
                created_date=created_date,
                campus=campus,
                views=views,
                more_link=more_link,
            )
