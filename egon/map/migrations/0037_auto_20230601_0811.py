# Generated by Django 3.2.18 on 2023-06-01 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0036_auto_20230530_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadarea',
            name='el_consumption',
            field=models.FloatField(null=True, verbose_name='Annual demand (MWh)'),
        ),
        migrations.AlterField(
            model_name='loadarea',
            name='el_peakload',
            field=models.FloatField(null=True, verbose_name='Max. demand (MW)'),
        ),
    ]