# Generated by Django 2.1.2 on 2018-11-04 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0018_auto_20181104_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='cur_operating',
            field=models.IntegerField(null=True, verbose_name='cur_operating'),
        ),
        migrations.AlterField(
            model_name='college',
            name='hispanic',
            field=models.IntegerField(null=True, verbose_name='hispanic'),
        ),
        migrations.AlterField(
            model_name='college',
            name='men_only',
            field=models.IntegerField(null=True, verbose_name='men_only'),
        ),
        migrations.AlterField(
            model_name='college',
            name='online_only',
            field=models.IntegerField(null=True, verbose_name='online_only'),
        ),
        migrations.AlterField(
            model_name='college',
            name='predom_black',
            field=models.IntegerField(null=True, verbose_name='predom_black'),
        ),
        migrations.AlterField(
            model_name='college',
            name='women_only',
            field=models.IntegerField(null=True, verbose_name='women_only'),
        ),
    ]
