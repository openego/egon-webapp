# Generated by Django 3.2.18 on 2023-04-21 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0009_demandcts_demandheatinghhcts_demandhousehold'),
    ]

    operations = [
        migrations.AddField(
            model_name='mvgriddistricts',
            name='bus_id',
            field=models.IntegerField(default=None, null=True),
            preserve_default=False,
        ),
    ]
