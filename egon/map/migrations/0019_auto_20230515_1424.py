# Generated by Django 3.2.18 on 2023-05-15 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0018_auto_20230515_1345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transportmitdemand',
            name='mv_grid_district',
        ),
        migrations.DeleteModel(
            name='DemandHousehold',
        ),
        migrations.DeleteModel(
            name='MVGridDistricts',
        ),
        migrations.DeleteModel(
            name='TransportMitDemand',
        ),
    ]
