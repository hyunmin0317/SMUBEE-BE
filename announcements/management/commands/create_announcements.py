from django.core.management import BaseCommand
from announcements import models as announcement_models
import requests
from bs4 import BeautifulSoup as bs


class Command(BaseCommand):
    def handle(self, *args, **options):

        url = "https://www.smu.ac.kr/lounge/notice/notice.do?mode=list&&articleLimit=1000&article.offset=0"
        src = requests.get(url).text
        soup = bs(src, "html.parser")
        data_list = soup.find("ul", {"class": "board-thumb-wrap"}).select("li > dl")

        for data in data_list:
            pinned = False
            content_title = data.select("dt > table > tbody > td")
            if content_title[0].find("span", {"class": "noti"}):
                pinned = True

            campus = announcement_models.Announcement.CAMPUS_BOTH
            campus_value = content_title[1].find("span", {"class": "cmp"})["class"]
            if "seoul" in campus_value:
                campus = announcement_models.Announcement.CAMPUS_SEO
            elif "cheon" in campus_value:
                campus = announcement_models.Announcement.CAMPUS_CHEO

            title = content_title[2].find("a").text.strip()

            content_info = data.select("dd > ul > li")
            number = int(content_info[0].text[4:].strip())
            created_date = content_info[2].text[4:].strip()
            views = int(content_info[3].text[4:].strip())
            more_link = f"https://www.smu.ac.kr/lounge/notice/notice.do?mode=view&articleNo={number}"

            announcement_models.Announcement.objects.create(
                title=title,
                pinned=pinned,
                number=number,
                created_date=created_date,
                campus=campus,
                views=views,
                more_link=more_link,
            )

        self.stdout.write(
            self.style.SUCCESS(f"{len(data_list)} announcements created!")
        )
