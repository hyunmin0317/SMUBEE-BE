# Generated by Django 3.2.6 on 2021-08-08 01:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0005_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
