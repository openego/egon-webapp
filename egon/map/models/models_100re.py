from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from egon.map.managers import MVTManager
from egon.map.models.abstract_models import (
    DemandModel,
    LineModel,
    SubstationModel,
    SupplyPlantModel,
    SupplyPotentialModel,
)

scenario_name = "egon100re"


# DEMAND
class LoadArea100RE(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    el_peakload = models.FloatField(null=True, verbose_name=_("Max. demand (MW)"))
    el_consumption = models.FloatField(null=True, verbose_name=_("Annual demand (MWh)"))

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "1_Demand"
    data_file = scenario_name + ".demand.electricity_load_areas"
    layer = data_file
    mapping = {"geom": "MULTIPOLYGON", "el_peakload": "el_peakload", "el_consumption": "el_consumption"}


class GasCH4Industry100RE(DemandModel):
    data_file = scenario_name + ".demand.gas_methane_for_industry"
    layer = data_file


class GasH2Industry100RE(DemandModel):
    data_file = scenario_name + ".demand.gas_hydrogen_for_industry"
    layer = data_file


class TransportHeavyDuty100RE(DemandModel):
    data_file = scenario_name + ".demand.transport_heavy-duty_transport"
    layer = data_file


class HeatingHouseholdsCts100RE(DemandModel):
    max = models.FloatField(null=True, verbose_name=_("Maximal demand (MW)"))
    min = models.FloatField(null=True, verbose_name=_("Minimal demand (MW)"))
    mapping = {"geom": "MULTIPOLYGON", "annual_demand": "annual_demand", "max": "max", "min": "min"}

    data_file = scenario_name + ".demand.heat_district_heating_households_and_cts"
    layer = data_file


# POTENTIALS
class CentralHeatPumps100RE(SupplyPotentialModel):
    capacity = models.FloatField(verbose_name=_("Electrical capacity (MW))"), null=True)
    data_file = scenario_name + ".supply.heat_central_heat_pumps"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "capacity": "capacity",
    }


class HeatGeothermal100RE(SupplyPotentialModel):
    capacity = models.FloatField(verbose_name=_("Electrical capacity (MW))"), null=True)
    data_file = scenario_name + ".supply.heat_geothermal"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "capacity": "capacity",
    }


class HeatSolarthermal100RE(SupplyPotentialModel):
    capacity = models.FloatField(verbose_name=_("Electrical capacity (MW))"), null=True)
    data_file = scenario_name + ".supply.heat_solarthermal"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "capacity": "capacity",
    }


class GasPotentialBiogasProduction100RE(SupplyPotentialModel):
    p_nom = models.FloatField(verbose_name=_("P nom"), null=True)
    data_file = scenario_name + ".supply.gas_potential_biogas_production"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "p_nom": "p_nom",
    }


class PVGroundMountedPotentialAreaAgriculture100RE(SupplyPotentialModel):
    area_km2 = models.FloatField(verbose_name=_("Potential area (km²)"), null=True)
    data_file = scenario_name + ".supply.pv_ground-mounted_potential_areas_agriculture"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "area_km2": "area_km2",
    }


class PVGroundMountedPotentialAreaHighways_Railroads100RE(SupplyPotentialModel):
    area_km2 = models.FloatField(verbose_name=_("Potential area (km²)"), null=True)
    data_file = scenario_name + ".supply.pv_ground-mounted_potential_areas_highways_&_railroad"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "area_km2": "area_km2",
    }


class WindOnshorePotentialArea100RE(SupplyPotentialModel):
    area_km2 = models.FloatField(verbose_name=_("Potential area (km²)"), null=True)
    data_file = scenario_name + ".supply.wind_onshore_potential_areas"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "area_km2": "area_km2",
    }


# POWER PLANTS
class WindOffshoreWindPark100RE(SupplyPlantModel):
    el_capacity = models.FloatField(verbose_name=_("Electrical Capacity"))
    voltage_level = models.PositiveIntegerField(verbose_name=_("Voltage level"))
    data_file = scenario_name + ".supply.wind_offshore_wind_parks"
    layer = data_file
    mapping = {"geom": "POINT", "el_capacity": "el_capacity", "voltage_level": "voltage_level"}


class WindOnshoreWindPark100RE(SupplyPlantModel):
    el_capacity = models.FloatField(verbose_name=_("Electrical Capacity"))
    voltage_level = models.PositiveIntegerField(verbose_name="Voltage level")
    data_file = scenario_name + ".supply.wind_onshore_wind_parks"
    layer = data_file
    mapping = {"geom": "POINT", "el_capacity": "el_capacity", "voltage_level": "voltage_level"}


class PVGroundMountedPVPlant100RE(SupplyPlantModel):
    el_capacity = models.FloatField(verbose_name=_("Electrical Capacity"))
    voltage_level = models.PositiveIntegerField(verbose_name="Voltage level")
    data_file = scenario_name + ".supply.pv_ground-mounted_pv_plants"
    layer = data_file
    mapping = {"geom": "POINT", "el_capacity": "el_capacity", "voltage_level": "voltage_level"}


class PVRoofTopPVPlantManager100RE(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(el_capacity__gt=0.13)


class PVRoofTopPVPlant100RE(SupplyPlantModel):
    el_capacity = models.FloatField(_("Electrical Capacity"))
    voltage_level = models.PositiveIntegerField(verbose_name="Voltage level")

    objects = PVRoofTopPVPlantManager100RE()
    data_file = scenario_name + ".supply.pv_roof-top_pv_plants"
    layer = data_file
    mapping = {"geom": "POINT", "el_capacity": "el_capacity", "voltage_level": "voltage_level"}


# POWER AND GAS GRIDS
class MVGridDistrictData100RE(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    area = models.FloatField(null=True)

    # DEMAND
    demand_population_sum = models.FloatField(verbose_name=_("Population"), null=True)

    demand_electricity_households_sum = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_electricity_households_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)
    demand_electricity_households_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)

    demand_electricity_cts_sum = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_electricity_cts_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)
    demand_electricity_cts_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)

    demand_electricity_industry_sum = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_electricity_industry_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)
    demand_electricity_industry_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)

    demand_heat_individual_heating_households_and_cts_sum = models.FloatField(
        verbose_name=_("Annual Demand (MWh)"), null=True
    )
    demand_heat_individual_heating_households_and_cts_max = models.FloatField(
        verbose_name=_("Maximal hourly demand (MW)"), null=True
    )
    demand_heat_individual_heating_households_and_cts_min = models.FloatField(
        verbose_name=_("Minimal hourly demand (MW)"), null=True
    )

    demand_transport_mit_number_of_evs_ev_count = models.IntegerField(
        verbose_name=_("Number of electric vehicles"), null=True
    )
    demand_transport_mit_number_of_evs_bev_mini = models.IntegerField(verbose_name=_("Number of compact EV"), null=True)
    demand_transport_mit_number_of_evs_bev_medium = models.IntegerField(
        verbose_name=_("Number of mid-range EV"), null=True
    )
    demand_transport_mit_number_of_evs_bev_luxury = models.IntegerField(
        verbose_name=_("Number of luxury-class EV"), null=True
    )
    demand_transport_mit_number_of_evs_phev_mini = models.IntegerField(
        verbose_name=_("Number of compact PHEV"), null=True
    )
    demand_transport_mit_number_of_evs_phev_medium = models.IntegerField(
        verbose_name=_("Number of mid-range PHEV"), null=True
    )
    demand_transport_mit_number_of_evs_phev_luxury = models.IntegerField(
        verbose_name=_("Number of luxury-class PHEV"), null=True
    )

    demand_transport_mit_demand_annual_demand = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_transport_mit_demand_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)
    demand_transport_mit_demand_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)

    # SUPPLY
    supply_wind_onshore_installed_capacity_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_wind_onshore_installed_capacity_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )
    supply_wind_onshore_potential_el_production_feedin = models.FloatField(
        verbose_name=_("Potential el. prodcution feed-in (MW)"), null=True
    )
    supply_wind_offshore_installed_capacity_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_wind_offshore_installed_capacity_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )
    supply_wind_offshore_potential_el_production_feedin = models.FloatField(
        verbose_name=_("Potential el. prodcution feed-in (MW)"), null=True
    )

    supply_pv_ground_mounted_installed_capacity_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_pv_ground_mounted_installed_capacity_unit_count = models.IntegerField(
        verbose_name=_("Number of power plants"), null=True
    )
    supply_pv_ground_mounted_potential_el_production_feedin = models.FloatField(
        verbose_name=_("Potential el. prodcution feed-in (MW)"), null=True
    )

    supply_pv_roof_top_installed_capacity_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_pv_roof_top_installed_capacity_unit_count = models.IntegerField(
        verbose_name=_("Number of power plants"), null=True
    )
    supply_pv_roof_top_potential_electricity_production_feedin = models.FloatField(
        verbose_name=_("Potential el. prodcution feed-in (MW)"), null=True
    )

    supply_other_gas_fired_power_plants_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_other_gas_fired_power_plants_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )

    supply_other_biomass_fired_power_plants_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_other_biomass_fired_power_plants_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )

    supply_other_hydro_el_capacity = models.FloatField(verbose_name=_("Installed capacity (MW)"), null=True)
    supply_other_hydro_unit_count = models.FloatField(verbose_name=_("Number of power plants"), null=True)

    supply_other_other_power_plants_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_other_other_power_plants_unit_count = models.FloatField(verbose_name=_("Number of power plants"), null=True)

    supply_heat_individual_heat_pumps_capacity = models.FloatField(verbose_name=_("Installed capacity (MW)"), null=True)

    flexibility_potential_electricity_dsm_dsm_potential = models.FloatField(
        verbose_name=_("Demand Side Potential (MW)"), null=True
    )

    flex_pot_electricity_electromobility_flex_demand = models.FloatField(
        verbose_name=_("Flexible demand (MW)"), null=True
    )
    flex_pot_electricity_electromobility_charging_demand = models.FloatField(
        verbose_name=_("Charging demand (MWh)"), null=True
    )
    flex_pot_electricity_electromobility_flex_share = models.FloatField(
        verbose_name=_("Share of flexible demand (%)"), null=True
    )

    flexibility_potential_storage_pumped_storage_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    flexibility_potential_storage_pumped_storage_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )
    flexibility_potential_storage_home_storage_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    flexibility_potential_storage_home_storage_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "3_Power_and_gas_grids"
    data_file = scenario_name + ".grid.egon_mv_grid_district"
    layer = data_file
    mapping = {
        "area": "area",
        "demand_electricity_households_sum": "demand_electricity_households_sum",
        "demand_electricity_households_max": "demand_electricity_households_max",
        "demand_electricity_households_min": "demand_electricity_households_min",
        "demand_population_sum": "demand_population_sum",
        "demand_transport_mit_number_of_evs_ev_count": "demand_transport_mit_number_of_evs_ev_count",
        "demand_transport_mit_number_of_evs_bev_mini": "demand_transport_mit_number_of_evs_bev_mini",
        "demand_transport_mit_number_of_evs_bev_medium": "demand_transport_mit_number_of_evs_bev_medium",
        "demand_transport_mit_number_of_evs_bev_luxury": "demand_transport_mit_number_of_evs_bev_luxury",
        "demand_transport_mit_number_of_evs_phev_mini": "demand_transport_mit_number_of_evs_phev_mini",
        "demand_transport_mit_number_of_evs_phev_medium": "demand_transport_mit_number_of_evs_phev_medium",
        "demand_transport_mit_number_of_evs_phev_luxury": "demand_transport_mit_number_of_evs_phev_luxury",
        "demand_transport_mit_demand_annual_demand": "demand_transport_mit_demand_annual_demand",
        "demand_transport_mit_demand_max": "demand_transport_mit_demand_max",
        "demand_transport_mit_demand_min": "demand_transport_mit_demand_min",
        "flex_pot_electricity_electromobility_charging_demand": "flexibility_potential_electricity_electromobility_charging_demand",  # noqa: E501
        "flex_pot_electricity_electromobility_flex_demand": "flexibility_potential_electricity_electromobility_flex_demand",  # noqa: E501
        "flex_pot_electricity_electromobility_flex_share": "flexibility_potential_electricity_electromobility_flex_share",  # noqa: E501
        "supply_other_biomass_fired_power_plants_el_capacity": "supply_other_biomass-fired_power_plants_el_capacity",
        "supply_other_biomass_fired_power_plants_unit_count": "supply_other_biomass-fired_power_plants_unit_count",
        "supply_other_gas_fired_power_plants_el_capacity": "supply_other_gas-fired_power_plants_el_capacity",
        "supply_other_gas_fired_power_plants_unit_count": "supply_other_gas-fired_power_plants_unit_count",
        "supply_other_hydro_el_capacity": "supply_other_hydro_el_capacity",
        "supply_other_hydro_unit_count": "supply_other_hydro_unit_count",
        "supply_other_other_power_plants_el_capacity": "supply_other_other_power_plants_el_capacity",
        "supply_other_other_power_plants_unit_count": "supply_other_other_power_plants_unit_count",
        "supply_pv_ground_mounted_installed_capacity_el_capacity": "supply_pv_ground-mounted_installed_capacity_el_capacity",  # noqa: E501
        "supply_pv_ground_mounted_installed_capacity_unit_count": "supply_pv_ground-mounted_installed_capacity_unit_count",  # noqa: E501
        "supply_pv_roof_top_installed_capacity_el_capacity": "supply_pv_roof-top_installed_capacity_el_capacity",
        "supply_pv_roof_top_installed_capacity_unit_count": "supply_pv_roof-top_installed_capacity_unit_count",
        "supply_wind_onshore_installed_capacity_el_capacity": "supply_wind_onshore_installed_capacity_el_capacity",
        "supply_wind_onshore_installed_capacity_unit_count": "supply_wind_onshore_installed_capacity_unit_count",
        "demand_electricity_cts_max": "demand_electricity_cts_max",
        "demand_electricity_cts_min": "demand_electricity_cts_min",
        "demand_electricity_cts_sum": "demand_electricity_cts_sum",
        "demand_electricity_industry_max": "demand_electricity_industry_max",
        "demand_electricity_industry_min": "demand_electricity_industry_min",
        "demand_electricity_industry_sum": "demand_electricity_industry_sum",
        "demand_heat_individual_heating_households_and_cts_max": "demand_heat_individual_heating_households_and_cts_max",  # noqa: E501
        "demand_heat_individual_heating_households_and_cts_min": "demand_heat_individual_heating_households_and_cts_min",  # noqa: E501
        "demand_heat_individual_heating_households_and_cts_sum": "demand_heat_individual_heating_households_and_cts_sum",  # noqa: E501
        "flexibility_potential_electricity_dsm_dsm_potential": "flexibility_potential_electricity_dsm_dsm_potential",
        "flexibility_potential_storage_home_storage_el_capacity": "flexibility_potential_storage_home_storage_el_capacity",  # noqa: E501
        "flexibility_potential_storage_home_storage_unit_count": "flexibility_potential_storage_home_storage_unit_count",  # noqa: E501
        "flexibility_potential_storage_pumped_storage_el_capacity": "flexibility_potential_storage_pumped_storage_el_capacity",  # noqa: E501
        "flexibility_potential_storage_pumped_storage_unit_count": "flexibility_potential_storage_pumped_storage_unit_count",  # noqa: E501
        "supply_heat_individual_heat_pumps_capacity": "supply_heat_individual_heat_pumps_capacity",
        "supply_pv_ground_mounted_potential_el_production_feedin": "supply_pv_ground-mounted_potential_electricity_production_feedin",  # noqa: E501
        "supply_pv_roof_top_potential_electricity_production_feedin": "supply_pv_roof-top_potential_electricity_production_feedin",  # noqa: E501
        "supply_wind_offshore_installed_capacity_el_capacity": "supply_wind_offshore_installed_capacity_el_capacity",
        "supply_wind_offshore_installed_capacity_unit_count": "supply_wind_offshore_installed_capacity_unit_count",
        "supply_wind_offshore_potential_el_production_feedin": "supply_wind_offshore_potential_electricity_production_feedin",  # noqa: E501
        "supply_wind_onshore_potential_el_production_feedin": "supply_wind_onshore_potential_electricity_production_feedin",  # noqa: E501
        "geom": "MULTIPOLYGON",
    }


class CH4Voronoi100RE(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "3_Power_and_gas_grids"
    mapping = {
        "geom": "MULTIPOLYGON",
    }

    data_file = scenario_name + ".grids.methane_voronoi"
    layer = data_file


class H2Voronoi100RE(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "3_Power_and_gas_grids"
    data_file = scenario_name + ".grids.hydrogen_voronoi"
    layer = data_file

    mapping = {
        "geom": "MULTIPOLYGON",
    }


class EHVLine100RE(LineModel):
    data_file = scenario_name + ".grids.electricity_ehv_lines"
    layer = data_file


class HVLine100RE(LineModel):
    data_file = scenario_name + ".grids.electricity_hv_lines"
    layer = data_file


class MethaneGridLine100RE(LineModel):
    data_file = scenario_name + ".grids.gas_methane_grid"
    layer = data_file


class FlexPotElDynamicLineRating100RE(LineModel):
    dlr = models.PositiveIntegerField(null=True)
    data_folder = "4_Flexibility"
    data_file = scenario_name + ".flexibility_potential.electricity_dynamic_line_rating"
    layer = data_file
    vector_tiles = MVTManager(columns=["id", "dlr"])

    mapping = {"geom": "MULTILINESTRING", "dlr": "dlr"}


class EHVHVSubstation100RE(SubstationModel):
    data_file = scenario_name + ".grids.electricity_ehv_hv_stations"
    layer = scenario_name + ".grids.electricity_ehv_hv_stations"


class HVMVSubstation100RE(SubstationModel):
    data_file = scenario_name + ".grids.electricity_hv_mv_stations"
    layer = scenario_name + ".grids.electricity_hv_mv_stations"


# FLEXIBILTY POTENTIAL
class PotentialH2UndergroundStorage100RE(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    e_nom_max = models.FloatField(null=True, verbose_name=_("Storage Capacity (MWh)"))

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "4_Flexibility"
    mapping = {
        "geom": "MULTIPOLYGON",
        "e_nom_max": "e_nom_max",
    }

    data_file = scenario_name + ".flexibility_potential.gas_potential_hydrogen_underground_storage"
    layer = data_file


class PotentialCH4Stores100RE(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    e_nom = models.FloatField(null=True, verbose_name=_("Storage Capacity (MWh)"))

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "4_Flexibility"
    mapping = {
        "geom": "MULTIPOLYGON",
        "e_nom": "e_nom",
    }

    data_file = scenario_name + ".flexibility_potential.gas_methane_stores"
    layer = data_file
