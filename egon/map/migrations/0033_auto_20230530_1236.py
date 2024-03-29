# Generated by Django 3.2.18 on 2023-05-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0032_auto_20230530_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heatinghouseholdscts',
            name='max',
            field=models.FloatField(null=True, verbose_name='Maximal demand (MW)'),
        ),
        migrations.AlterField(
            model_name='heatinghouseholdscts',
            name='min',
            field=models.FloatField(null=True, verbose_name='Minimal demand (MW)'),
        ),
    ]
