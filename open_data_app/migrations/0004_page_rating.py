# Generated by Django 2.1.2 on 2019-12-25 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('open_data_app', '0003_auto_20190831_0610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('top_text', models.TextField(blank=True)),
                ('bottom_text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='open_data_app.Page')),
                ('colleges', models.ManyToManyField(to='open_data_app.College')),
            ],
            bases=('open_data_app.page',),
        ),
    ]
