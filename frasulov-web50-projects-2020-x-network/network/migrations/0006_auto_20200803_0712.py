# Generated by Django 3.0.8 on 2020-08-03 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20200803_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(related_name='likes', to='network.NetworkUser'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
