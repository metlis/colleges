# Generated by Django 2.1.2 on 2018-11-03 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0005_college_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='city_slug',
            field=models.SlugField(blank=True),
        ),
    ]
