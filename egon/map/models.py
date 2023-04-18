from dataclasses import dataclass
from enum import Enum

from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CenterMVTManager, LabelMVTManager, MVTManager, RegionMVTManager


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
# DEMAND
class DemandModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    demand = models.IntegerField()

    objects = models.Manager()
    vector_tiles = CenterMVTManager(columns=["id", "demand", "lat", "lon"])

    data_folder = "1_Demand"
    mapping = {
        "geom": "MULTIPOLYGON",
        "demand": "demand",
    }

    class Meta:
        abstract = True


class DemandCts(DemandModel):
    data_file = "egon_demand_electricity_cts_2035"
    layer = "egon_demand_electricity_cts_2035"

    class Meta:
        verbose_name = _("Demand CTS")
        verbose_name_plural = _("Demands CTS")


class DemandHousehold(DemandModel):
    data_file = "egon_demand_electricity_household_2035"
    layer = "egon_demand_electricity_household_2035"

    class Meta:
        verbose_name = _("Demand Household")
        verbose_name_plural = _("Demands Household")


class DemandHeatingHhCts(DemandModel):
    data_file = "demand.egon_district_heating_areas"
    layer = "demand.egon_district_heating_areas"

    class Meta:
        verbose_name = _("Demand Heating Household and CTS")
        verbose_name_plural = _("Demand Heating Household and CTS")


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


# DATA MODEL


class MVGridDistricts(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    area = models.FloatField()

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id", "area"])

    data_folder = "4_Data_model"
    data_file = "grid.egon_mv_grid_district"
    layer = "grid.egon_mv_grid_district"
    mapping = {"geom": "MULTIPOLYGON", "area": "area"}
