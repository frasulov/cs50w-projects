# Generated by Django 3.0.8 on 2020-07-24 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200724_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='auctions', to='auctions.Category'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='created',
            field=models.CharField(default='July 24, 2020 09:19:55', max_length=64),
        ),
        migrations.AlterField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='bids', to='auctions.Auction'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='my_bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='auctions.Auction'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='my_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='watcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]