# Generated by Django 3.2.18 on 2023-05-05 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0015_remove_mvgriddistricts_area'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DemandCts',
        ),
        migrations.DeleteModel(
            name='DemandHeatingHhCts',
        ),
    ]
