# Generated by Django 2.1.2 on 2018-10-28 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0004_auto_20181028_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='url',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
