from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from django.shortcuts import render

def login(id, password):
    URL = "https://ecampus.smu.ac.kr/login.php"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver = webdriver.Chrome('/home/sangmyung/chromedriver', options=options)
    driver.get(URL)
    driver.find_element(By.ID, 'input-username').send_keys(id)
    driver.find_element(By.ID, 'input-password').send_keys(password)
    driver.find_element(By.NAME, 'loginbutton').click()
    return driver.page_source

def course(id, password):
    data = []
    url = login(id, password)
    soup = BeautifulSoup(url, 'html.parser')
    courses = soup.find_all("div", class_="course-title")
    for course in courses:
        dic = {'name':course.find("h3").text, 'prof':course.find("p").text}
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