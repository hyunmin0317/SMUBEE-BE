from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def login(id, password):
    URL = "https://ecampus.smu.ac.kr/login.php"
    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)
    driver.find_element(By.ID, 'input-username').send_keys(id)
    driver.find_element(By.ID, 'input-password').send_keys(password)
    driver.find_element(By.NAME, 'loginbutton').click()
    return driver.page_source

def course():
    data = []
    url = login("201911019", "password")
    soup = BeautifulSoup(url, 'html.parser')
    courses = soup.find_all("div", class_="course_box")
    for course in courses:
        dic = {'name':course.find("h3").text, 'prof':course.find("p").text, 'code':course.find("a")["href"].split("=")[1]}
        data.append(dic)
    return data

if __name__ == '__main__':
    courses = course()

    if len(courses)==0:
        print("로그인 실패")
    else:
        for course in courses:
            print(course['name'], course['prof'], course['code'])