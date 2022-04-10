from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.shortcuts import render
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver = webdriver.Chrome('/home/ubuntu/chromedriver', options=options)

def login(id, password):
    URL = "https://ecampus.smu.ac.kr/login.php"
    driver.get(URL)
    driver.find_element(By.ID, 'input-username').send_keys(id)
    driver.find_element(By.ID, 'input-password').send_keys(password)
    driver.find_element(By.NAME, 'loginbutton').click()

def logout():
    url = "https://ecampus.smu.ac.kr/login/logout.php?sesskey=743L2Q8XQd"
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="notice"]/div/div[1]/form/div/input[1]').click()

def subject():
    url = "https://ecampus.smu.ac.kr"
    driver.get(url)
    page = driver.page_source
    data = []

    soup = BeautifulSoup(page, 'html.parser')
    subjects = soup.find_all("div", class_="course_box")
    for subject in subjects:
        dic = {'name': subject.find("h3").text, 'prof': subject.find("p").text,
               'code': subject.find("a")["href"].split("=")[1]}
        data.append(dic)
    return data

def course(code):
    url = "https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id=" + code
    driver.get(url)
    page = driver.page_source
    data = []

    soup = BeautifulSoup(page, 'html.parser')
    body = soup.find("table", class_="user_progress")

    if body is not None:
        courses = body.find_all("td", class_="text-left")
        for course in courses:
            data.append(course.text)
    return data

def home(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']
        login(id, password)
        subjects = subject()
        # logout()

        if len(subjects) == 0:
            print("로그인 실패")
            return render(request, 'login.html')
        else:
            context = {'subjects': subjects}
            return render(request, 'home.html', context)

def detail(request, code):
    context = {'code':code, 'courses':course(code)}
    return render(request, 'detail.html', context)
