# Generated by Django 3.1.1 on 2020-12-21 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201221_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='image_url',
            field=models.URLField(blank=True, default=''),
        ),
    ]