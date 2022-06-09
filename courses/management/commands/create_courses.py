from django.core.management import BaseCommand
from courses import models as course_models
from professors import models as professor_models
from openpyxl import load_workbook


class Command(BaseCommand):
    def handle(self, *args, **options):

        wb = load_workbook("2021-01-courses.xlsx")
        ws = wb.active

        for row in ws.iter_rows():
            course_code, class_number = row[0].value.split("-")
            title = row[1].value
            pfs = row[3].value.split(",")
            for pf in pfs:
                professor = professor_models.Professor.objects.get_or_create(name=pf)
                
            # course_models.Course.objects.create(

            # )
            # print(course_code, class_number, title, professor)

        # self.stdout.write(self.style.SUCCESS(f"{len(data_list)} professors created!"))
