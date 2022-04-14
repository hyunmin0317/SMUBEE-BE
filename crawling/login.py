import requests
from bs4 import BeautifulSoup as bs

#beautifulsoup대신 bs 사용하겠다는 뜻
user_info = { 'username' : '201911019', 'password' : '1q2w3e4r!!' }

with requests.Session() as s:
    request = s.post('https://ecampus.smu.ac.kr/login/index.php', data=user_info)
    source = request.text
    soup = bs(source,'html.parser')

    top_list = soup.select("#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a > div.course-name > div.course-title > h3")
    print("강의 목록\n")
    for top in top_list:
        print(top.text)