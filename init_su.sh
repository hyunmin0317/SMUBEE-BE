#!/bin/sh

echo "------ create default admin user ------"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('hyunmin', 'choihm9903@naver.com', 'cc990317')" | python manage.py shell