# Generated by Django 2.1.2 on 2019-12-25 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0007_auto_20191225_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='name',
            field=models.CharField(default='kjhljhlkj', max_length=255),
            preserve_default=False,
        ),
    ]
