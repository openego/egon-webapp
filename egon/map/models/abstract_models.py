from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from egon.map.managers import MVTManager


# DEMAND
class DemandModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    annual_demand = models.FloatField(null=True, verbose_name=_("Annual demand (MWh)"))

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "1_Demand"
    mapping = {
        "geom": "MULTIPOLYGON",
        "annual_demand": "annual_demand",
    }

    class Meta:
        abstract = True


# SUPPLY
# POTENTIALS
class SupplyPotentialModel(models.Model):
    geom = models.MultiPolygonField(srid=4326)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "2_Supply"

    class Meta:
        abstract = True


# POWER PLANTS
class SupplyPlantModel(models.Model):
    geom = models.PointField(srid=4326)

    objects = models.Manager()
    vector_tiles = MVTManager(columns=["id"])

    data_folder = "2_Supply"

    class Meta:
        abstract = True


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
