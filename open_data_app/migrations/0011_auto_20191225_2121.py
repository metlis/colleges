# Generated by Django 2.1.2 on 2019-12-25 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0010_filter_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='parameter_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='filter',
            name='parameter_value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
