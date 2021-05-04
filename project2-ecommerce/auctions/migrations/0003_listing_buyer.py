# Generated by Django 3.1.1 on 2021-03-09 18:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_current_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='buyer',
            field=models.ManyToManyField(null=True, related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
    ]
