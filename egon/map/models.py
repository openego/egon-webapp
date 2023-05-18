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


class MVGridDistrictData(models.Model):
    geom = models.MultiPolygonField(srid=4326, null=True)
    area = models.FloatField(null=True)

    # Demand Electricity Households
    demand_electricity_households_2035_sum = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_electricity_households_2035_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)
    demand_electricity_households_2035_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)

    demand_electricity_households_100RE_sum = models.FloatField(verbose_name=_("Annual Demand (MWh)"), null=True)
    demand_electricity_households_100RE_min = models.FloatField(verbose_name=_("Minimal hourly demand (MW)"), null=True)
    demand_electricity_households_100RE_max = models.FloatField(verbose_name=_("Maximal hourly demand (MW)"), null=True)

    # Demand Transport mit Number of EV
    transport_mit_number_of_evs_2035_ev_count = models.IntegerField(
        verbose_name=_("Number of electric vehicles"), null=True
    )
    transport_mit_number_of_evs_2035_bev_mini = models.IntegerField(verbose_name=_("Number of compact EV"), null=True)
    transport_mit_number_of_evs_2035_bev_medium = models.IntegerField(
        verbose_name=_("Number of mid-range EV"), null=True
    )
    transport_mit_number_of_evs_2035_bev_luxury = models.IntegerField(
        verbose_name=_("Number of luxury-class EV"), null=True
    )
    transport_mit_number_of_evs_2035_phev_mini = models.IntegerField(
        verbose_name=_("Number of compact PHEV"), null=True
    )
    transport_mit_number_of_evs_2035_phev_medium = models.IntegerField(
        verbose_name=_("Number of mid-range PHEV"), null=True
    )
    transport_mit_number_of_evs_2035_phev_luxury = models.IntegerField(
        verbose_name=_("Number of luxury-class PHEV"), null=True
    )
    transport_mit_number_of_evs_100RE_ev_count = models.IntegerField(
        verbose_name=_("Number of electric vehicles"), null=True
    )
    transport_mit_number_of_evs_100RE_bev_mini = models.IntegerField(verbose_name=_("Number of compact EV"), null=True)
    transport_mit_number_of_evs_100RE_bev_medium = models.IntegerField(
        verbose_name=_("Number of mid-range EV"), null=True
    )
    transport_mit_number_of_evs_100RE_bev_luxury = models.IntegerField(
        verbose_name=_("Number of luxury-class EV"), null=True
    )
    transport_mit_number_of_evs_100RE_phev_mini = models.IntegerField(
        verbose_name=_("Number of compact PHEV"), null=True
    )
    transport_mit_number_of_evs_100RE_phev_medium = models.IntegerField(
        verbose_name=_("Number of mid-range PHEV"), null=True
    )
    transport_mit_number_of_evs_100RE_phev_luxury = models.IntegerField(
        verbose_name=_("Number of luxury-class PHEV"), null=True
    )

    # Demand Transport mit Number of EV
    supply_pv_ground_mounted_installed_capacity_2035_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_pv_ground_mounted_installed_capacity_2035_unit_count = models.IntegerField(
        verbose_name=_("Number of power plants"), null=True
    )

    supply_pv_ground_mounted_installed_capacity_100RE_el_capacity = models.FloatField(
        verbose_name=_("Installed capacity (MW)"), null=True
    )
    supply_pv_ground_mounted_installed_capacity_100RE_unit_count = models.IntegerField(
        verbose_name=_("Number of power plants"), null=True
    )

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_file = "MERGED_grid.egon_mv_grid_district"
    layer = "MEGA_grid.egon_mv_grid_district"
    mapping = {
        "geom": "MULTIPOLYGON",
        "id": "bus_id",
        "demand_electricity_households_2035_sum": "demand_electricity_households_2035_sum",
        "demand_electricity_households_2035_min": "demand_electricity_households_2035_min",
        "demand_electricity_households_2035_max": "demand_electricity_households_2035_max",
        "demand_electricity_households_100RE_sum": "demand_electricity_households_100RE_sum",
        "demand_electricity_households_100RE_min": "demand_electricity_households_100RE_min",
        "demand_electricity_households_100RE_max": "demand_electricity_households_100RE_max",
        "transport_mit_number_of_evs_2035_ev_count": "transport_mit_number_of_evs_2035_ev_count",
        "transport_mit_number_of_evs_2035_bev_mini": "transport_mit_number_of_evs_2035_bev_mini",
        "transport_mit_number_of_evs_2035_bev_medium": "transport_mit_number_of_evs_2035_bev_medium",
        "transport_mit_number_of_evs_2035_bev_luxury": "transport_mit_number_of_evs_2035_bev_luxury",
        "transport_mit_number_of_evs_2035_phev_mini": "transport_mit_number_of_evs_2035_phev_mini",
        "transport_mit_number_of_evs_2035_phev_medium": "transport_mit_number_of_evs_2035_phev_medium",
        "transport_mit_number_of_evs_2035_phev_luxury": "transport_mit_number_of_evs_2035_phev_luxury",
        "transport_mit_number_of_evs_100RE_ev_count": "transport_mit_number_of_evs_100RE_ev_count",
        "transport_mit_number_of_evs_100RE_bev_mini": "transport_mit_number_of_evs_100RE_bev_mini",
        "transport_mit_number_of_evs_100RE_bev_medium": "transport_mit_number_of_evs_100RE_bev_medium",
        "transport_mit_number_of_evs_100RE_bev_luxury": "transport_mit_number_of_evs_100RE_bev_luxury",
        "transport_mit_number_of_evs_100RE_phev_mini": "transport_mit_number_of_evs_100RE_phev_mini",
        "transport_mit_number_of_evs_100RE_phev_medium": "transport_mit_number_of_evs_100RE_phev_medium",
        "transport_mit_number_of_evs_100RE_phev_luxury": "transport_mit_number_of_evs_100RE_phev_luxury",
        "supply_pv_ground_mounted_installed_capacity_2035_el_capacity": "supply_pv_ground_mounted_installed_capacity"
        "_2035_el_capacity",
        "supply_pv_ground_mounted_installed_capacity_2035_unit_count": "supply_pv_ground_mounted_installed_capacity"
        "_2035_unit_count",
        "supply_pv_ground_mounted_installed_capacity_100RE_el_capacity": "supply_pv_ground_mounted_installed_capacity"
        "_100RE_el_capacity",
        "supply_pv_ground_mounted_installed_capacity_100RE_unit_count": "supply_pv_ground_mounted_installed_capacity"
        "_100RE_unit_count",
    }


class MapLayer(models.Model):
    scenario = models.CharField(
        max_length=5,
        choices=[("2035", "2035"), ("100RE", "100RE"), (_("both"), "both")],
        default="2035",
    )
    identifier = models.CharField(max_length=64)
    geom_layer = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256, blank=True, null=True)
    colors = ArrayField(models.CharField(max_length=64), null=True, blank=True)
    icon = models.CharField(max_length=32, null=True, blank=True)
    choropleth_field = models.CharField(max_length=64, blank=True, null=True)
    popup_fields = ArrayField(models.CharField(max_length=64), null=True, blank=True)
    popup_title = models.CharField(max_length=64, null=True, blank=True)
    popup_description = models.CharField(max_length=1024, null=True, blank=True)
    category = models.CharField(
        max_length=16,
        choices=[
            ("demand", _("Demand")),
            ("supply", _("Supply")),
            ("grids", _("Grids")),
            ("model", _("Data Model")),
        ],
        default="demand",
    )
    sub_category = models.CharField(
        max_length=64, null=True, blank=True, help_text="Create subcategories for the display in the frontend."
    )

    def __str__(self):
        return self.get_category_display() + ": " + self.name + " (" + self.scenario + ")"

    class Meta:
        verbose_name = _("Map Layer")
        verbose_name_plural = _("Map Layers")


class SupplyModel(models.Model):
    geom = models.PointField(srid=4326)
    carrier = models.CharField(max_length=255)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id", "carrier"])

    data_folder = "2_Supply"
    mapping = {
        "geom": "POINT",
        "carrier": "carrier",
    }

    class Meta:
        abstract = True


class SupplyBiomass(SupplyModel):
    data_file = "egon_supply_power_plants_biomass"
    layer = "egon_supply_power_plants_biomass"


class SupplyRunOfRiver(SupplyModel):
    data_file = "egon_supply_power_plants_run_of_river"
    layer = "egon_supply_power_plants_run_of_river"


class SupplySolarGround(SupplyModel):
    data_file = "egon_supply_power_plants_solar_ground"
    layer = "egon_supply_power_plants_solar_ground"


class SupplyWindOnshore(SupplyModel):
    data_file = "egon_supply_power_plants_wind_onshore"
    layer = "egon_supply_power_plants_wind_onshore"


class SupplyPotentialModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "2_Supply"
    mapping = {
        "geom": "MULTIPOLYGON",
    }

    class Meta:
        abstract = True


class SupplyPotentialPVGround(SupplyPotentialModel):
    data_file = "egon_supply_re_potential_areas_pvground"
    layer = "egon_supply_re_potential_areas_pvground"


class SupplyPotentialWind(SupplyPotentialModel):
    geom_data_field = "geom"
    choropleth_data_field = ""
    data_file = "egon_supply_re_potential_areas_wind"
    layer = "egon_supply_re_potential_areas_wind"


# POWER AND GAS GRIDS


class LineModel(models.Model):
    geom = models.MultiLineStringField(srid=4326)
    type = models.CharField(max_length=255)
    carrier = models.CharField(max_length=255)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id", "type", "carrier"])

    data_folder = "3_Power_and_gas_grids"
    mapping = {
        "geom": "MULTILINESTRING",
    }

    class Meta:
        abstract = True


class EHVLine(LineModel):
    data_file = "egon_grid_ehv_line_2035"
    layer = "egon_grid_ehv_line_2035"


class HVLine(LineModel):
    data_file = "egon_grid_hv_line_2035"
    layer = "egon_grid_hv_line_2035"


class SubstationModel(models.Model):
    geom = models.PointField(srid=4326)
    voltage = models.CharField(max_length=255)
    power_type = models.CharField(max_length=255)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id", "voltage", "power_type"])

    data_folder = "3_Power_and_gas_grids"
    mapping = {
        "geom": "POINT",
    }

    class Meta:
        abstract = True


class EHVHVSubstation(SubstationModel):
    data_file = "egon_grid_ehvhv_substation"
    layer = "egon_grid_ehvhv_substation"


class HVMVSubstation(SubstationModel):
    data_file = "egon_grid_hvmv_substation"
    layer = "egon_grid_hvmv_substation"
