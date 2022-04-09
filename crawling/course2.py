from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def login(id, password):
    url = "https://ecampus.smu.ac.kr/login.php"
    driver.get(url)

    driver.find_element(By.ID, 'input-username').send_keys(id)
    driver.find_element(By.ID, 'input-password').send_keys(password)
    driver.find_element(By.NAME, 'loginbutton').click()

def course():
    url = "https://ecampus.smu.ac.kr"
    driver.get(url)
    page = driver.page_source
    data = []

    soup = BeautifulSoup(page, 'html.parser')
    courses = soup.find_all("div", class_="course_box")
    for course in courses:
        dic = {'name':course.find("h3").text, 'prof':course.find("p").text, 'code':course.find("a")["href"].split("=")[1]}
        data.append(dic)
    return data

def course_data(code):
    url = "https://ecampus.smu.ac.kr/report/ubcompletion/user_progress.php?id="+code
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    body = soup.find("table", class_="user_progress")
    courses = body.find_all("td", class_="text-left")

    for course in courses:
        print(course)
        print(type(course))
        print(course.find("td"))


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    login("201911019", "1q2w3e4r!!")
    courses = course()
    course_data("68630")

    if len(courses)==0:
        print("로그인 실패")
    else:
        for course in courses:
            print(course['name'], course['prof'], course['code'])