# Generated by Django 3.1.1 on 2021-01-06 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0030_auto_20210106_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='user_who_made_last_successful_bid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
