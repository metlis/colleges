# Generated by Django 2.1.2 on 2019-08-30 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='slug',
            field=models.SlugField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='state',
            name='slug',
            field=models.SlugField(blank=True, max_length=255),
        ),
    ]
