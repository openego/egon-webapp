# Generated by Django 3.2.18 on 2023-07-18 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0047_ch4voronoi100re_ehvhvsubstation100re_ehvline100re_flexpoteldynamiclinerating100re_h2voronoi100re_hvl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_cts_100re_max',
            new_name='demand_electricity_cts_max',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_cts_100re_min',
            new_name='demand_electricity_cts_min',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_cts_100re_sum',
            new_name='demand_electricity_cts_sum',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_households_100re_max',
            new_name='demand_electricity_households_max',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_households_100re_min',
            new_name='demand_electricity_households_min',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_households_100re_sum',
            new_name='demand_electricity_households_sum',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_industry_100re_max',
            new_name='demand_electricity_industry_max',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_industry_100re_min',
            new_name='demand_electricity_industry_min',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_electricity_industry_100re_sum',
            new_name='demand_electricity_industry_sum',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_heat_individual_heating_households_and_cts_100re_max',
            new_name='demand_heat_individual_heating_households_and_cts_max',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_heat_individual_heating_households_and_cts_100re_min',
            new_name='demand_heat_individual_heating_households_and_cts_min',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_heat_individual_heating_households_and_cts_100re_sum',
            new_name='demand_heat_individual_heating_households_and_cts_sum',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_population_100re_sum',
            new_name='demand_population_sum',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_demand_100re_annual_demand',
            new_name='demand_transport_mit_demand_annual_demand',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_demand_100re_max',
            new_name='demand_transport_mit_demand_max',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_demand_100re_min',
            new_name='demand_transport_mit_demand_min',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_number_of_evs_100re_bev_luxury',
            new_name='demand_transport_mit_number_of_evs_bev_luxury',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_number_of_evs_100re_bev_medium',
            new_name='demand_transport_mit_number_of_evs_bev_medium',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_number_of_evs_100re_bev_mini',
            new_name='demand_transport_mit_number_of_evs_bev_mini',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_number_of_evs_100re_ev_count',
            new_name='demand_transport_mit_number_of_evs_ev_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_number_of_evs_100re_phev_luxury',
            new_name='demand_transport_mit_number_of_evs_phev_luxury',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_number_of_evs_100re_phev_medium',
            new_name='demand_transport_mit_number_of_evs_phev_medium',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='demand_transport_mit_number_of_evs_100re_phev_mini',
            new_name='demand_transport_mit_number_of_evs_phev_mini',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='flex_pot_electricity_electromobility_100re_charging_demand',
            new_name='flex_pot_electricity_electromobility_charging_demand',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='flex_pot_electricity_electromobility_100re_flex_demand',
            new_name='flex_pot_electricity_electromobility_flex_demand',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='flex_pot_electricity_electromobility_100re_flex_share',
            new_name='flex_pot_electricity_electromobility_flex_share',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='flexibility_potential_electricity_dsm_100re_dsm_potential',
            new_name='flexibility_potential_electricity_dsm_dsm_potential',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='flexibility_potential_storage_home_storage_100re_el_capacity',
            new_name='flexibility_potential_storage_home_storage_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='flexibility_potential_storage_home_storage_100re_unit_count',
            new_name='flexibility_potential_storage_home_storage_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='flexibility_potential_storage_pumped_storage_100re_el_capacity',
            new_name='flexibility_potential_storage_pumped_storage_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='flexibility_potential_storage_pumped_storage_100re_unit_count',
            new_name='flexibility_potential_storage_pumped_storage_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_heat_individual_heat_pumps_100re_capacity',
            new_name='supply_heat_individual_heat_pumps_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_other_biomass_fired_power_plants_100re_el_capacity',
            new_name='supply_other_biomass_fired_power_plants_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_other_biomass_fired_power_plants_100re_unit_count',
            new_name='supply_other_biomass_fired_power_plants_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_other_gas_fired_power_plants_100re_el_capacity',
            new_name='supply_other_gas_fired_power_plants_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_other_gas_fired_power_plants_100re_unit_count',
            new_name='supply_other_gas_fired_power_plants_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_other_hydro_100re_el_capacity',
            new_name='supply_other_hydro_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_other_hydro_100re_unit_count',
            new_name='supply_other_hydro_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_other_other_power_plants_100re_el_capacity',
            new_name='supply_other_other_power_plants_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_other_other_power_plants_100re_unit_count',
            new_name='supply_other_other_power_plants_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_pv_ground_mounted_installed_capacity_100re_el_capacity',
            new_name='supply_pv_ground_mounted_installed_capacity_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_pv_ground_mounted_installed_capacity_100re_unit_count',
            new_name='supply_pv_ground_mounted_installed_capacity_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_pv_ground_mounted_potential_el_production_100re_feedin',
            new_name='supply_pv_ground_mounted_potential_el_production_feedin',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_pv_roof_top_installed_capacity_100re_el_capacity',
            new_name='supply_pv_roof_top_installed_capacity_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_pv_roof_top_installed_capacity_100re_unit_count',
            new_name='supply_pv_roof_top_installed_capacity_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_wind_offshore_installed_capacity_100re_el_capacity',
            new_name='supply_wind_offshore_installed_capacity_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_wind_offshore_installed_capacity_100re_unit_count',
            new_name='supply_wind_offshore_installed_capacity_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_wind_offshore_potential_el_production_100re_feedin',
            new_name='supply_wind_offshore_potential_el_production_feedin',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_wind_onshore_installed_capacity_100re_el_capacity',
            new_name='supply_wind_onshore_installed_capacity_el_capacity',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_wind_onshore_installed_capacity_100re_unit_count',
            new_name='supply_wind_onshore_installed_capacity_unit_count',
        ),
        migrations.RenameField(
            model_name='mvgriddistrictdata100re',
            old_name='supply_wind_onshore_potential_el_production_100re_feedin',
            new_name='supply_wind_onshore_potential_el_production_feedin',
        ),
    ]