# Generated by Django 3.2.18 on 2023-05-30 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0034_auto_20230530_1457'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mvgriddistrictdata',
            old_name='supply_pv_ground_mounted_potential_electricity_production_2035_feedin',
            new_name='supply_pv_ground_mounted_potential_el_production_2035_feedin',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata',
            old_name='supply_wind_offshore_potential_electricity_production_2035_feedin',
            new_name='supply_wind_offshore_potential_el_production_2035_feedin',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata',
            old_name='supply_wind_onshore_potential_electricity_production_2035_feedin',
            new_name='supply_wind_onshore_potential_el_production_2035_feedin',
        ),
    ]
