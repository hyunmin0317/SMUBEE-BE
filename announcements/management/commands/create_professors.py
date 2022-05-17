from django.core.management import BaseCommand
from professors import models as professor_models
import requests
from bs4 import BeautifulSoup as bs


class Command(BaseCommand):
    def handle(self, *args, **options):

        url = "https://www.smu.ac.kr/ko/edu/Profile.do?mode=list&pagerLimit=500"
        src = requests.get(url).text
        soup = bs(src, "html.parser")
        data_list = soup.select(
            "#jwxe_main_content > div > div > div > div > ul > li > div.texts"
        )

        for data in data_list:
            lis = data.find_all("li")
            name = data.find("strong").text
            office, contact_number = None, None
            for li in lis:
                if "연구실" in li.text:
                    office = li.text[6:]
                if "연락처" in li.text:
                    contact_number = li.text[6:]
            more_link = (
                "https://www.smu.ac.kr/ko/edu/Profile.do"
                + data.find("a", {"class": "more"}, href=True)["href"]
            )
            email = data.find("a", {"class": "btn_massage"}, href=True)["href"][7:]

            professor_models.Professor.objects.create(
                name=name,
                office=office,
                email=email,
                contact_number=contact_number,
                more_link=more_link,
            )

        self.stdout.write(self.style.SUCCESS(f"{len(data_list)} professors created!"))
