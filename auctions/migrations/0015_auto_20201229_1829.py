# Generated by Django 3.1.1 on 2020-12-29 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20201227_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctions',
            name='starting_bid',
        ),
        migrations.AddField(
            model_name='bids',
            name='auction',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='auction', to='auctions.auctions'),
        ),
        migrations.AddField(
            model_name='bids',
            name='last_bid',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bids',
            name='starting_bid',
            field=models.IntegerField(default=0),
        ),
    ]
