import requests
from bs4 import BeautifulSoup as bs

def subject(id, password):
    user_info = {'username': id, 'password': password}
    data = []

    with requests.Session() as s:
        request = s.post('https://ecampus.smu.ac.kr/login/index.php', data=user_info)
        source = request.text
        soup = bs(source,'html.parser')

        name_list = soup.select("#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a > div.course-name > div.course-title > h3")
        prof_list = soup.select("#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a > div.course-name > div.course-title > p")
        code_list = soup.select("#region-main > div > div.progress_courses > div.course_lists > ul > li > div > a")

        for name, prof, code in zip(name_list, prof_list, code_list):
            dic = {'name': name.text, 'prof': prof.text, 'code': code["href"].split("=")[1]}
            data.append(dic)
    return data


if __name__ == '__main__':
    subject_list = subject('201911019', 'password')
    print(subject_list)