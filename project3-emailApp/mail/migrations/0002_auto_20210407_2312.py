# Generated by Django 3.1.1 on 2021-04-07 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='body',
            field=models.TextField(),
        ),
    ]
