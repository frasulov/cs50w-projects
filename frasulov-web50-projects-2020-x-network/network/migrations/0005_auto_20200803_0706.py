# Generated by Django 3.0.8 on 2020-08-03 07:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_comment_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='is_like',
        ),
        migrations.AlterField(
            model_name='networkuser',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='follower_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='networkuser',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
