# Generated by Django 3.0.8 on 2020-08-03 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20200803_0823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='newone',
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='network.NetworkUser'),
        ),
    ]
