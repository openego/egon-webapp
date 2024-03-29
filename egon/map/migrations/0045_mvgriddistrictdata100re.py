# Generated by Django 3.2.18 on 2023-06-29 10:06

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0044_pvgroundmountedpvplant100re_pvrooftoppvplant100re_windoffshorewindpark100re_windonshorewindpark100re'),
    ]

    operations = [
        migrations.CreateModel(
            name='MVGridDistrictData100RE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('area', models.FloatField(null=True)),
                ('demand_population_100re_sum', models.FloatField(null=True, verbose_name='Population')),
                ('demand_electricity_households_100re_sum', models.FloatField(null=True, verbose_name='Annual Demand (MWh)')),
                ('demand_electricity_households_100re_max', models.FloatField(null=True, verbose_name='Maximal hourly demand (MW)')),
                ('demand_electricity_households_100re_min', models.FloatField(null=True, verbose_name='Minimal hourly demand (MW)')),
                ('demand_electricity_cts_100re_sum', models.FloatField(null=True, verbose_name='Annual Demand (MWh)')),
                ('demand_electricity_cts_100re_max', models.FloatField(null=True, verbose_name='Maximal hourly demand (MW)')),
                ('demand_electricity_cts_100re_min', models.FloatField(null=True, verbose_name='Minimal hourly demand (MW)')),
                ('demand_electricity_industry_100re_sum', models.FloatField(null=True, verbose_name='Annual Demand (MWh)')),
                ('demand_electricity_industry_100re_max', models.FloatField(null=True, verbose_name='Maximal hourly demand (MW)')),
                ('demand_electricity_industry_100re_min', models.FloatField(null=True, verbose_name='Minimal hourly demand (MW)')),
                ('demand_heat_individual_heating_households_and_cts_100re_sum', models.FloatField(null=True, verbose_name='Annual Demand (MWh)')),
                ('demand_heat_individual_heating_households_and_cts_100re_max', models.FloatField(null=True, verbose_name='Maximal hourly demand (MW)')),
                ('demand_heat_individual_heating_households_and_cts_100re_min', models.FloatField(null=True, verbose_name='Minimal hourly demand (MW)')),
                ('demand_transport_mit_number_of_evs_100re_ev_count', models.IntegerField(null=True, verbose_name='Number of electric vehicles')),
                ('demand_transport_mit_number_of_evs_100re_bev_mini', models.IntegerField(null=True, verbose_name='Number of compact EV')),
                ('demand_transport_mit_number_of_evs_100re_bev_medium', models.IntegerField(null=True, verbose_name='Number of mid-range EV')),
                ('demand_transport_mit_number_of_evs_100re_bev_luxury', models.IntegerField(null=True, verbose_name='Number of luxury-class EV')),
                ('demand_transport_mit_number_of_evs_100re_phev_mini', models.IntegerField(null=True, verbose_name='Number of compact PHEV')),
                ('demand_transport_mit_number_of_evs_100re_phev_medium', models.IntegerField(null=True, verbose_name='Number of mid-range PHEV')),
                ('demand_transport_mit_number_of_evs_100re_phev_luxury', models.IntegerField(null=True, verbose_name='Number of luxury-class PHEV')),
                ('demand_transport_mit_demand_100re_annual_demand', models.FloatField(null=True, verbose_name='Annual Demand (MWh)')),
                ('demand_transport_mit_demand_100re_max', models.FloatField(null=True, verbose_name='Maximal hourly demand (MW)')),
                ('demand_transport_mit_demand_100re_min', models.FloatField(null=True, verbose_name='Minimal hourly demand (MW)')),
                ('supply_wind_onshore_installed_capacity_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('supply_wind_onshore_installed_capacity_100re_unit_count', models.FloatField(null=True, verbose_name='Number of power plants')),
                ('supply_wind_onshore_potential_el_production_100re_feedin', models.FloatField(null=True, verbose_name='Potential el. prodcution feed-in (MW)')),
                ('supply_wind_offshore_installed_capacity_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('supply_wind_offshore_installed_capacity_100re_unit_count', models.FloatField(null=True, verbose_name='Number of power plants')),
                ('supply_wind_offshore_potential_el_production_100re_feedin', models.FloatField(null=True, verbose_name='Potential el. prodcution feed-in (MW)')),
                ('supply_pv_ground_mounted_installed_capacity_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('supply_pv_ground_mounted_installed_capacity_100re_unit_count', models.IntegerField(null=True, verbose_name='Number of power plants')),
                ('supply_pv_ground_mounted_potential_el_production_100re_feedin', models.FloatField(null=True, verbose_name='Potential el. prodcution feed-in (MW)')),
                ('supply_pv_roof_top_installed_capacity_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('supply_pv_roof_top_installed_capacity_100re_unit_count', models.IntegerField(null=True, verbose_name='Number of power plants')),
                ('supply_pv_roof_top_potential_electricity_production_100re_feedin', models.FloatField(null=True, verbose_name='Potential el. prodcution feed-in (MW)')),
                ('supply_other_gas_fired_power_plants_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('supply_other_gas_fired_power_plants_100re_unit_count', models.FloatField(null=True, verbose_name='Number of power plants')),
                ('supply_other_biomass_fired_power_plants_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('supply_other_biomass_fired_power_plants_100re_unit_count', models.FloatField(null=True, verbose_name='Number of power plants')),
                ('supply_other_hydro_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('supply_other_hydro_100re_unit_count', models.FloatField(null=True, verbose_name='Number of power plants')),
                ('supply_other_other_power_plants_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('supply_other_other_power_plants_100re_unit_count', models.FloatField(null=True, verbose_name='Number of power plants')),
                ('supply_heat_individual_heat_pumps_100re_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('flexibility_potential_electricity_dsm_100re_dsm_potential', models.FloatField(null=True, verbose_name='Demand Side Potential (MW)')),
                ('flex_pot_electricity_electromobility_100re_flex_demand', models.FloatField(null=True, verbose_name='Flexible demand (MW)')),
                ('flex_pot_electricity_electromobility_100re_charging_demand', models.FloatField(null=True, verbose_name='Charging demand (MWh)')),
                ('flex_pot_electricity_electromobility_100re_flex_share', models.FloatField(null=True, verbose_name='Share of flexible demand (%)')),
                ('flexibility_potential_storage_pumped_storage_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('flexibility_potential_storage_pumped_storage_100re_unit_count', models.FloatField(null=True, verbose_name='Number of power plants')),
                ('flexibility_potential_storage_home_storage_100re_el_capacity', models.FloatField(null=True, verbose_name='Installed capacity (MW)')),
                ('flexibility_potential_storage_home_storage_100re_unit_count', models.FloatField(null=True, verbose_name='Number of power plants')),
            ],
        ),
    ]
