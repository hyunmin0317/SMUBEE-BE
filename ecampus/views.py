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
    return driver.page_source

def course(id, password):
    data = []
    url = login(id, password)
    soup = BeautifulSoup(url, 'html.parser')
    courses = soup.find_all("div", class_="course_box")
    for course in courses:
        dic = {'name':course.find("h3").text, 'prof':course.find("p").text, 'code':course.find("a")["href"].split("=")[1]}
        data.append(dic)
    return data


def home(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        id = request.POST['id']
        password = request.POST['password']
        courses = course(id, password)

        if len(courses) == 0:
            print("로그인 실패")
            return render(request, 'login.html')
        else:
            context = {'courses': courses}
            return render(request, 'home.html', context)

def detail(request, code):
    context = {'code':code}
    return render(request, 'detail.html', context)
