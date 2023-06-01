from dataclasses import dataclass
from enum import Enum

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from .managers import LabelMVTManager, MVTManager, RegionMVTManager


class LayerFilterType(Enum):
    Range = 0
    Dropdown = 1


@dataclass
class LayerFilter:
    name: str
    type: LayerFilterType = LayerFilterType.Range


# REGIONS
class Region(models.Model):
    """Base class for all regions - works as connector to other models"""

    class LayerType(models.TextChoices):
        COUNTRY = "country", _("Country")
        STATE = "state", _("State")
        DISTRICT = "district", _("District")
        MUNICIPALITY = "municipality", _("Municipality")

    layer_type = models.CharField(max_length=12, choices=LayerType.choices, null=False)


class RegionModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)

    region = models.OneToOneField("Region", on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_folder = "0_Boundaries"
    data_file = "egon_boundaries_country"
    layer = "egon_boundaries_country"
    mapping = {
        "geom": "MULTIPOLYGON",
        "name": "gen",
    }

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Country(RegionModel):
    data_file = "egon_boundaries_country"
    layer = "egon_boundaries_country"


class State(RegionModel):
    data_file = "egon_boundaries_state"
    layer = "egon_boundaries_state"


class District(RegionModel):
    name = models.CharField(max_length=50)

    data_file = "egon_boundaries_district"
    layer = "egon_boundaries_district"


class Municipality(RegionModel):
    name = models.CharField(max_length=50)

    data_file = "egon_boundaries_municipality"
    layer = "egon_boundaries_municipality"


# LAYER
class MapLayer(models.Model):
    scenario = models.CharField(
        max_length=5,
        choices=[("2035", "2035"), ("100RE", "100RE"), (_("both"), "both")],
        help_text="Identifies the scenario. Use 'both' if there is no difference.",
    )
    identifier = models.CharField(
        max_length=64, help_text="Only used internally to be able to activte layer with javascript."
    )
    geom_layer = models.CharField(
        max_length=64, blank=True, null=True, help_text="The identifier of the layer that holds the geom."
    )
    name = models.CharField(max_length=64, help_text="The name used for display in the frontend.")
    description = models.CharField(
        max_length=1024,
        blank=True,
        null=True,
        help_text="The description that can be found in the frontend, when clicking on the info-icon.",
    )
    colors = ArrayField(
        models.CharField(max_length=64),
        null=True,
        blank=True,
        help_text="One ore multiple (for choropleths) colors for the display in the frontend.",
    )
    icon = models.CharField(max_length=32, null=True, blank=True, help_text="If an icon should be displayed.")
    choropleth_field = models.CharField(
        max_length=64, blank=True, null=True, help_text="The field that holds the data for the choropleth."
    )
    choropleth_unit = models.CharField(max_length=64, null=True, blank=True)
    popup_fields = ArrayField(
        models.CharField(max_length=64),
        null=True,
        blank=True,
        help_text="The comma-seperated field(s), that should be displayed inside the popup.",
    )
    popup_title = models.CharField(
        max_length=64, null=True, blank=True, help_text="The title of the popup. Defaults to 'name'."
    )
    popup_description = models.CharField(
        max_length=1024, null=True, blank=True, help_text="The description of the popup. Defaults to 'description'."
    )
    category = models.CharField(
        max_length=16,
        choices=[
            ("demand", _("Demand")),
            ("supply", _("Supply")),
            ("grids", _("Grids")),
            ("model", _("Data Model")),
        ],
        default="demand",
        help_text="The main category in the left panel in the frontend.",
    )
    sub_category = models.CharField(
        max_length=64, null=True, blank=True, help_text="The sub-category for the display in the frontend."
    )
    data_model = models.CharField(max_length=64, help_text="The name of the model that holds the data.")

    data_file = "maplayer"

    def __str__(self):
        return self.get_category_display() + ": " + self.name + " (" + self.scenario + ")"

    class Meta:
        verbose_name = _("Map Layer")
        verbose_name_plural = _("Map Layers")


# DEMAND
class LoadArea(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    el_peakload = models.FloatField(null=True, verbose_name=_("Max. demand (MW)"))
    el_consumption = models.FloatField(null=True, verbose_name=_("Annual demand (MWh)"))

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "1_Demand"
    data_file = "egon2035.demand.electricity_load_areas"
    layer = "egon2035.demand.electricity_load_areas_"
    mapping = {"geom": "MULTIPOLYGON", "el_peakload": "el_peakload", "el_consumption": "el_consumption"}


class DemandModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    annual_demand = models.FloatField(null=True)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "1_Demand"
    mapping = {
        "geom": "MULTIPOLYGON",
        "annual_demand": "annual_demand",
    }

    class Meta:
        abstract = True


class GasCH4Industry(DemandModel):
    data_file = "egon2035.demand.gas_methane_for_industry"
    layer = data_file


class GasH2Industry(DemandModel):
    data_file = "egon2035.demand.gas_hydrogen_for_industry"
    layer = data_file


class TransportHeavyDuty(DemandModel):
    data_file = "egon2035.demand.transport_heavy-duty_transport"
    layer = data_file


class HeatingHouseholdsCts(DemandModel):
    max = models.FloatField(null=True, verbose_name=_("Maximal demand (MW)"))
    min = models.FloatField(null=True, verbose_name=_("Minimal demand (MW)"))
    mapping = {
        "geom": "MULTIPOLYGON",
        "annual_demand": "annual_demand",
    }

    data_file = "egon2035.demand.heat_district_heating_households_and_cts"
    layer = data_file


# SUPPLY
# POTENTIALS
class SupplyPotentialModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "2_Supply"

    class Meta:
        abstract = True


class CentralHeatPumps(SupplyPotentialModel):
    capacity = models.FloatField(verbose_name=_("Electrical capacity (MW))"), null=True)
    data_file = "egon2035.supply.heat_central_heat_pumps"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "capacity": "capacity",
    }


class HeatGeothermal(SupplyPotentialModel):
    capacity = models.FloatField(verbose_name=_("Electrical capacity (MW))"), null=True)
    data_file = "egon2035.supply.heat_geothermal"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "capacity": "capacity",
    }


class HeatSolarthermal(SupplyPotentialModel):
    capacity = models.FloatField(verbose_name=_("Electrical capacity (MW))"), null=True)
    data_file = "egon2035.supply.heat_solarthermal"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "capacity": "capacity",
    }


class GasPotentialBiogasProduction(SupplyPotentialModel):
    p_nom = models.FloatField(verbose_name=_("P nom"), null=True)
    data_file = "egon2035.supply.gas_potential_biogas_production"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "p_nom": "p_nom",
    }


class GasPotentialNaturalGasProduction(SupplyPotentialModel):
    p_nom = models.FloatField(verbose_name=_("P nom (MWh)"), null=True)
    data_file = "egon2035.supply.gas_potential_natural_gas_production_"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "p_nom": "p_nom",
    }


class PVGroundMountedPotentialAreaAgriculture(SupplyPotentialModel):
    area_km2 = models.FloatField(verbose_name=_("Potential area (km²)"), null=True)
    data_file = "egon2035.supply.pv_ground-mounted_potential_areas_agriculture"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "area_km2": "area_km2",
    }


class PVGroundMountedPotentialAreaHighways_Railroads(SupplyPotentialModel):
    area_km2 = models.FloatField(verbose_name=_("Potential area (km²)"), null=True)
    data_file = "egon2035.supply.pv_ground-mounted_potential_areas_highways_&_railroad"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "area_km2": "area_km2",
    }


class WindOnshorePotentialArea(SupplyPotentialModel):
    area_km2 = models.FloatField(verbose_name=_("Potential area (km²)"), null=True)
    data_file = "egon2035.supply.wind_onshore_potential_areas"
    layer = data_file
    mapping = {
        "geom": "MULTIPOLYGON",
        "area_km2": "area_km2",
    }


# POWER PLANTS
class SupplyPlantModel(models.Model):
    geom = models.PointField(srid=4326)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "2_Supply"

    class Meta:
        abstract = True


class WindOffshoreWindPark(SupplyPlantModel):
    el_capacity = models.FloatField(verbose_name=_("Electrical Capacity"))
    voltage_level = models.PositiveIntegerField(verbose_name="Voltage level")
    data_file = "egon2035.supply.wind_offshore_wind_parks"
    layer = data_file
    mapping = {"geom": "POINT", "el_capacity": "el_capacity", "voltage_level": "voltage_level"}


class WindOnshoreWindPark(SupplyPlantModel):
    el_capacity = models.FloatField(verbose_name=_("Electrical Capacity"))
    voltage_level = models.PositiveIntegerField(verbose_name="Voltage level")
    data_file = "egon2035.supply.wind_onshore_wind_parks"
    layer = data_file
    mapping = {"geom": "POINT", "el_capacity": "el_capacity", "voltage_level": "voltage_level"}


class PVGroundMountedPVPlant(SupplyPlantModel):
    el_capacity = models.FloatField(verbose_name=_("Electrical Capacity"))
    voltage_level = models.PositiveIntegerField(verbose_name="Voltage level")
    data_file = "egon2035.supply.pv_ground-mounted_pv_plants"
    layer = data_file
    mapping = {"geom": "POINT", "el_capacity": "el_capacity", "voltage_level": "voltage_level"}


class PVRoofTopPVPlantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(el_capacity__gt=0.13)


class PVRoofTopPVPlant(SupplyPlantModel):
    el_capacity = models.FloatField(_("Electrical Capacity"))
    voltage_level = models.PositiveIntegerField(verbose_name="Voltage level")

    objects = PVRoofTopPVPlantManager()
    data_file = "egon2035.supply.pv_roof-top_pv_plants"
    layer = data_file
    mapping = {"geom": "POINT", "el_capacity": "el_capacity", "voltage_level": "voltage_level"}


# POWER AND GAS GRIDS
class MVGridDistrictData(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    area = models.FloatField(null=True)

    # DEMAND
    demand_population_2035_sum = models.FloatField(verbose_name=_("Population"), null=True)

    demand_electricity_households_2035_sum = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_electricity_households_2035_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)
    demand_electricity_households_2035_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)

    demand_electricity_cts_2035_sum = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_electricity_cts_2035_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)
    demand_electricity_cts_2035_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)

    demand_electricity_industry_2035_sum = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_electricity_industry_2035_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)
    demand_electricity_industry_2035_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)

    demand_heat_individual_heating_households_and_cts_2035_sum = models.FloatField(
        verbose_name=_("Annual Demand (MWh)"), null=True
    )
    demand_heat_individual_heating_households_and_cts_2035_max = models.FloatField(
        verbose_name=_("Maximal hourly demand (MW)"), null=True
    )
    demand_heat_individual_heating_households_and_cts_2035_min = models.FloatField(
        verbose_name=_("Minimal hourly demand (MW)"), null=True
    )

    demand_transport_mit_number_of_evs_2035_ev_count = models.IntegerField(
        verbose_name=_("Number of electric vehicles"), null=True
    )
    demand_transport_mit_number_of_evs_2035_bev_mini = models.IntegerField(
        verbose_name=_("Number of compact EV"), null=True
    )
    demand_transport_mit_number_of_evs_2035_bev_medium = models.IntegerField(
        verbose_name=_("Number of mid-range EV"), null=True
    )
    demand_transport_mit_number_of_evs_2035_bev_luxury = models.IntegerField(
        verbose_name=_("Number of luxury-class EV"), null=True
    )
    demand_transport_mit_number_of_evs_2035_phev_mini = models.IntegerField(
        verbose_name=_("Number of compact PHEV"), null=True
    )
    demand_transport_mit_number_of_evs_2035_phev_medium = models.IntegerField(
        verbose_name=_("Number of mid-range PHEV"), null=True
    )
    demand_transport_mit_number_of_evs_2035_phev_luxury = models.IntegerField(
        verbose_name=_("Number of luxury-class PHEV"), null=True
    )

    demand_transport_mit_demand_2035_annual_demand = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_transport_mit_demand_2035_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)
    demand_transport_mit_demand_2035_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)

    # SUPPLY
    supply_wind_onshore_installed_capacity_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_wind_onshore_installed_capacity_2035_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )
    supply_wind_onshore_potential_el_production_2035_feedin = models.FloatField(
        verbose_name=_("Potential el. prodcution feed-in (MW)"), null=True
    )
    supply_wind_offshore_installed_capacity_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_wind_offshore_installed_capacity_2035_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )
    supply_wind_offshore_potential_el_production_2035_feedin = models.FloatField(
        verbose_name=_("Potential el. prodcution feed-in (MW)"), null=True
    )

    supply_pv_ground_mounted_installed_capacity_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_pv_ground_mounted_installed_capacity_2035_unit_count = models.IntegerField(
        verbose_name=_("Number of power plants"), null=True
    )
    supply_pv_ground_mounted_potential_el_production_2035_feedin = models.FloatField(
        verbose_name=_("Potential el. prodcution feed-in (MW)"), null=True
    )

    supply_pv_roof_top_installed_capacity_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_pv_roof_top_installed_capacity_2035_unit_count = models.IntegerField(
        verbose_name=_("Number of power plants"), null=True
    )
    supply_pv_roof_top_potential_electricity_production_2035_feedin = models.FloatField(
        verbose_name=_("Potential el. prodcution feed-in (MW)"), null=True
    )

    supply_other_gas_fired_power_plants_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_other_gas_fired_power_plants_2035_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )

    supply_other_biomass_fired_power_plants_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_other_biomass_fired_power_plants_2035_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )

    supply_other_hydro_2035_el_capacity = models.FloatField(verbose_name=_("Installed capacity (MW)"), null=True)
    supply_other_hydro_2035_unit_count = models.FloatField(verbose_name=_("Number of power plants"), null=True)

    supply_other_other_power_plants_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_other_other_power_plants_2035_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )

    supply_heat_individual_heat_pumps_2035_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )

    flexibility_potential_electricity_dsm_2035_dsm_potential = models.FloatField(
        verbose_name=_("Demand Side Potential (MW)"), null=True
    )

    flex_pot_electricity_electromobility_2035_flex_demand = models.FloatField(
        verbose_name=_("Flexible demand (MW)"), null=True
    )
    flex_pot_electricity_electromobility_2035_charging_demand = models.FloatField(
        verbose_name=_("Charging demand (MWh)"), null=True
    )
    flex_pot_electricity_electromobility_2035_flex_share = models.FloatField(
        verbose_name=_("Share of flexible demand (%)"), null=True
    )

    flexibility_potential_storage_pumped_storage_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    flexibility_potential_storage_pumped_storage_2035_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )
    flexibility_potential_storage_home_storage_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    flexibility_potential_storage_home_storage_2035_unit_count = models.FloatField(
        verbose_name=_("Number of power plants"), null=True
    )

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "3_Power_and_gas_grids"
    data_file = "egon_2035.grids.egon_mv_grid_district"
    layer = "MERGED_grid.egon_mv_grid_district"
    mapping = {
        "area": "area",
        "demand_electricity_households_2035_sum": "demand_electricity_households_2035_sum",
        "demand_electricity_households_2035_max": "demand_electricity_households_2035_max",
        "demand_electricity_households_2035_min": "demand_electricity_households_2035_min",
        "demand_population_2035_sum": "demand_population_2035_sum",
        "demand_transport_mit_number_of_evs_2035_ev_count": "demand_transport_mit_number_of_evs_2035_ev_count",
        "demand_transport_mit_number_of_evs_2035_bev_mini": "demand_transport_mit_number_of_evs_2035_bev_mini",
        "demand_transport_mit_number_of_evs_2035_bev_medium": "demand_transport_mit_number_of_evs_2035_bev_medium",
        "demand_transport_mit_number_of_evs_2035_bev_luxury": "demand_transport_mit_number_of_evs_2035_bev_luxury",
        "demand_transport_mit_number_of_evs_2035_phev_mini": "demand_transport_mit_number_of_evs_2035_phev_mini",
        "demand_transport_mit_number_of_evs_2035_phev_medium": "demand_transport_mit_number_of_evs_2035_phev_medium",
        "demand_transport_mit_number_of_evs_2035_phev_luxury": "demand_transport_mit_number_of_evs_2035_phev_luxury",
        "demand_transport_mit_demand_2035_annual_demand": "demand_transport_mit_demand_2035_annual_demand",
        "demand_transport_mit_demand_2035_max": "demand_transport_mit_demand_2035_max",
        "demand_transport_mit_demand_2035_min": "demand_transport_mit_demand_2035_min",
        "flex_pot_electricity_electromobility_2035_charging_demand": "flexibility_potential_electricity_electromobility_2035_charging_demand",  # noqa: E501
        "flex_pot_electricity_electromobility_2035_flex_demand": "flexibility_potential_electricity_electromobility_2035_flex_demand",  # noqa: E501
        "flex_pot_electricity_electromobility_2035_flex_share": "flexibility_potential_electricity_electromobility_2035_flex_share",  # noqa: E501
        "supply_other_biomass_fired_power_plants_2035_el_capacity": "supply_other_biomass-fired_power_plants_2035_el_capacity",  # noqa: E501
        "supply_other_biomass_fired_power_plants_2035_unit_count": "supply_other_biomass-fired_power_plants_2035_unit_count",  # noqa: E501
        "supply_other_gas_fired_power_plants_2035_el_capacity": "supply_other_gas-fired_power_plants_2035_el_capacity",
        "supply_other_gas_fired_power_plants_2035_unit_count": "supply_other_gas-fired_power_plants_2035_unit_count",
        "supply_other_hydro_2035_el_capacity": "supply_other_hydro_2035_el_capacity",
        "supply_other_hydro_2035_unit_count": "supply_other_hydro_2035_unit_count",
        "supply_other_other_power_plants_2035_el_capacity": "supply_other_other_power_plants_2035_el_capacity",
        "supply_other_other_power_plants_2035_unit_count": "supply_other_other_power_plants_2035_unit_count",
        "supply_pv_ground_mounted_installed_capacity_2035_el_capacity": "supply_pv_ground-mounted_installed_capacity_2035_el_capacity",  # noqa: E501
        "supply_pv_ground_mounted_installed_capacity_2035_unit_count": "supply_pv_ground-mounted_installed_capacity_2035_unit_count",  # noqa: E501
        "supply_pv_roof_top_installed_capacity_2035_el_capacity": "supply_pv_roof-top_installed_capacity_2035_el_capacity",  # noqa: E501
        "supply_pv_roof_top_installed_capacity_2035_unit_count": "supply_pv_roof-top_installed_capacity_2035_unit_count",  # noqa: E501
        "supply_wind_onshore_installed_capacity_2035_el_capacity": "supply_wind_onshore_installed_capacity_2035_el_capacity",  # noqa: E501
        "supply_wind_onshore_installed_capacity_2035_unit_count": "supply_wind_onshore_installed_capacity_2035_unit_count",  # noqa: E501
        "demand_electricity_cts_2035_max": "demand_electricity_cts_2035_max",
        "demand_electricity_cts_2035_min": "demand_electricity_cts_2035_min",
        "demand_electricity_cts_2035_sum": "demand_electricity_cts_2035_sum",
        "demand_electricity_industry_2035_max": "demand_electricity_industry_2035_max",
        "demand_electricity_industry_2035_min": "demand_electricity_industry_2035_min",
        "demand_electricity_industry_2035_sum": "demand_electricity_industry_2035_sum",
        "demand_heat_individual_heating_households_and_cts_2035_max": "demand_heat_individual_heating_households_and_cts_2035_max",  # noqa: E501
        "demand_heat_individual_heating_households_and_cts_2035_min": "demand_heat_individual_heating_households_and_cts_2035_min",  # noqa: E501
        "demand_heat_individual_heating_households_and_cts_2035_sum": "demand_heat_individual_heating_households_and_cts_2035_sum",  # noqa: E501
        "flexibility_potential_electricity_dsm_2035_dsm_potential": "flexibility_potential_electricity_dsm_2035_dsm_potential",  # noqa: E501
        "flexibility_potential_storage_home_storage_2035_el_capacity": "flexibility_potential_storage_home_storage_2035_el_capacity",  # noqa: E501
        "flexibility_potential_storage_home_storage_2035_unit_count": "flexibility_potential_storage_home_storage_2035_unit_count",  # noqa: E501
        "flexibility_potential_storage_pumped_storage_2035_el_capacity": "flexibility_potential_storage_pumped_storage_2035_el_capacity",  # noqa: E501
        "flexibility_potential_storage_pumped_storage_2035_unit_count": "flexibility_potential_storage_pumped_storage_2035_unit_count",  # noqa: E501
        "supply_heat_individual_heat_pumps_2035_capacity": "supply_heat_individual_heat_pumps_2035_capacity",
        "supply_pv_ground_mounted_potential_el_production_2035_feedin": "supply_pv_ground-mounted_potential_electricity_production_2035_feedin",  # noqa: E501
        "supply_pv_roof_top_potential_electricity_production_2035_feedin": "supply_pv_roof-top_potential_electricity_production_2035_feedin",  # noqa: E501
        "supply_wind_offshore_installed_capacity_2035_el_capacity": "supply_wind_offshore_installed_capacity_2035_el_capacity",  # noqa: E501
        "supply_wind_offshore_installed_capacity_2035_unit_count": "supply_wind_offshore_installed_capacity_2035_unit_count",  # noqa: E501
        "supply_wind_offshore_potential_el_production_2035_feedin": "supply_wind_offshore_potential_electricity_production_2035_feedin",  # noqa: E501
        "supply_wind_onshore_potential_el_production_2035_feedin": "supply_wind_onshore_potential_electricity_production_2035_feedin",  # noqa: E501
        "geom": "MULTIPOLYGON",
    }


class CH4Voronoi(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    scn_name = models.CharField(max_length=64)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "3_Power_and_gas_grids"
    mapping = {
        "geom": "MULTIPOLYGON",
        "scn_name": "scn_name",
    }

    data_file = "grid.egon_gas_voronoi_ch4"
    layer = "grid.egon_gas_voronoi_ch4"


class H2Voronoi(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    scn_name = models.CharField(max_length=64)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "3_Power_and_gas_grids"
    mapping = {
        "geom": "MULTIPOLYGON",
        "scn_name": "scn_name",
    }

    data_file = "grid.egon_gas_voronoi_h2_grid"
    layer = "grid.egon_gas_voronoi_h2_grid"


class LineModel(models.Model):
    geom = models.MultiLineStringField(srid=4326)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "3_Power_and_gas_grids"
    mapping = {
        "geom": "MULTILINESTRING",
    }

    class Meta:
        abstract = True


class EHVLine(LineModel):
    data_file = "egon_grid_ehv_line_2035"
    layer = data_file


class HVLine(LineModel):
    data_file = "egon_grid_hv_line_2035"
    layer = data_file


class MethaneGridLine(LineModel):
    data_file = "egon2035.grids.gas_methane_grid"
    layer = data_file


class FlexPotElDynamicLineRating(LineModel):
    dlr = models.PositiveIntegerField(null=True)
    data_folder = "4_Flexibility"
    data_file = "egon2035.flexibility_potential.electricity_dynamic_line_rating"
    layer = data_file
    vector_tiles = MVTManager(columns=["id", "dlr"])

    mapping = {"geom": "MULTILINESTRING", "dlr": "dlr"}


class SubstationModel(models.Model):
    geom = models.PointField(srid=4326)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "3_Power_and_gas_grids"
    mapping = {
        "geom": "POINT",
    }

    class Meta:
        abstract = True


class EHVHVSubstation(SubstationModel):
    data_file = "egon2035.grids.electricity_ehv_hv_stations"
    layer = "egon2035.grids.electricity_ehv_hv_stations"


class HVMVSubstation(SubstationModel):
    data_file = "egon2035.grids.electricity_hv_mv_stations"
    layer = "egon2035.grids.electricity_hv_mv_stations"


# FLEXIBILTY POTENTIAL
class PotentialH2UndergroundStorage(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    e_nom_max = models.FloatField(null=True, verbose_name=_("Storage Capacity (MWh)"))

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "4_Flexibility"
    mapping = {
        "geom": "MULTIPOLYGON",
        "e_nom_max": "e_nom_max",
    }

    data_file = "egon2035.flexibility_potential.gas_potential_hydrogen_underground_storage"
    layer = data_file


class PotentialCH4Stores(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    e_nom = models.FloatField(null=True, verbose_name=_("Storage Capacity (MWh)"))

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "4_Flexibility"
    mapping = {
        "geom": "MULTIPOLYGON",
        "e_nom": "e_nom",
    }

    data_file = "egon2035.flexibility_potential.gas_methane_stores"
    layer = data_file
