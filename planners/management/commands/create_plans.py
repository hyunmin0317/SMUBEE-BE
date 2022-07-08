from django.core.management import BaseCommand
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs


class Command(BaseCommand):
    def handle(self, *args, **options):

        # 현재 나와있는 학사일정 연도 확인

        base_url = "https://www.smu.ac.kr/ko/life/academicCalendar.do?mode=list"
        url = "&srYear={year}&srMonth={month}"

        available_years = []

        src = requests.get(base_url).text
        soup = bs(src, "html.parser")
        year_list = soup.select(
            "#jwxe_main_content > div > div > .common-board .cal-or-list > select > option"
        )

        for year in year_list:
            available_years.append(year["value"])

        # 월별 크롤링

        for year in available_years:
            for month in range(1, 13):
                session = HTMLSession()
                url = f"https://www.smu.ac.kr/ko/life/academicCalendar.do?mode=list&srYear={year}&srMonth={month}"
                r = session.get(url)
                r.html.render()
                data_list = r.html.find(
                    "#jwxe_main_content > div > div > .common-board .month-schedule tbody > tr"
                )

                print(year, month)

                for data in data_list:
                    tds = data.find("td")
                    date_data = tds[0].text.replace(" ", "").split("~")
                    if date_data[0] == "일정없음":
                        continue
                    print(date_data)

                print("=" * 30)

        self.stdout.write(self.style.SUCCESS(f"{len(data_list)} professors created!"))
