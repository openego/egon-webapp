# Generated by Django 3.2.18 on 2023-05-17 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0022_auto_20230517_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='icon',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]