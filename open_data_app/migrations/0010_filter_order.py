# Generated by Django 2.1.2 on 2019-12-25 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0009_auto_20191225_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='order',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
