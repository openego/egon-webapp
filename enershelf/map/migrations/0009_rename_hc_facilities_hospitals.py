# Generated by Django 3.2.3 on 2021-06-14 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0008_alter_hc_facilities_nightlight_distance'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HC_Facilities',
            new_name='Hospitals',
        ),
    ]