# Generated by Django 3.1 on 2020-08-27 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineCourses', '0003_auto_20200827_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_text',
            field=models.TextField(blank=True),
        ),
    ]