
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .managers import MVTManager, RegionMVTManager, LabelMVTManager


# REGIONS

class Region(models.Model):
    """Base class for all regions - works as connector to other models"""

    class LayerType(models.TextChoices):
        COUNTRY = "country", _("Land")
        STATE = "state", _("Bundesland")
        DISTRICT = "district", _("Kreis")
        MUNICIPALITY = "municipality", _("Gemeinde")

    layer_type = models.CharField(max_length=12, choices=LayerType.choices, null=False)


class Country(models.Model):
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

    def __str__(self):
        return self.name


class State(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)

    region = models.OneToOneField("Region", on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_folder = "0_Boundaries"
    data_file = "egon_boundaries_state"
    layer = "egon_boundaries_state"
    mapping = {
        "geom": "MULTISURFACE",
        "name": "gen",
    }

    def __str__(self):
        return self.name


class District(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)

    region = models.OneToOneField("Region", on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_folder = "0_Boundaries"
    data_file = "egon_boundaries_district"
    layer = "egon_boundaries_district"
    mapping = {
        "geom": "MULTISURFACE",
        "name": "gen",
    }

    def __str__(self):
        return self.name


class Municipality(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)

    region = models.OneToOneField("Region", on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_folder = "0_Boundaries"
    data_file = "egon_boundaries_municipality"
    layer = "egon_boundaries_municipality"
    mapping = {
        "geom": "MULTISURFACE",
        "name": "gen",
    }

    def __str__(self):
        return self.name


# LAYER
