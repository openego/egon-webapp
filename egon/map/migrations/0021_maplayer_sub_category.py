# Generated by Django 3.2.18 on 2023-05-16 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0020_auto_20230516_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='sub_category',
            field=models.CharField(blank=True, help_text='Create subcategories for the display in the frontend.', max_length=64, null=True),
        ),
    ]
