# Generated by Django 3.2.18 on 2023-05-04 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0014_auto_20230503_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mvgriddistricts',
            name='area',
        ),
    ]
