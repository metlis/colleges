# Generated by Django 2.1.2 on 2018-11-03 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0012_auto_20181103_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='ownership',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='open_data_app.Ownership', verbose_name='ownership__name'),
        ),
    ]