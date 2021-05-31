from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from .managers import RegionMVTManager, LabelMVTManager


class Region(models.Model):
    """Base class for all regions - works as connector to other models"""

    class LayerType(models.TextChoices):
        COUNTRY = "country", _("Land")
        STATE = "state", _("Bundesland")
        DISTRICT = "district", _("Kreis")
        MUNICIPALITY = "municipality", _("Gemeinde")

    layer_type = models.CharField(max_length=12, choices=LayerType.choices, null=False)


# REGIONS


class Country(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=40)
    nuts = models.CharField(max_length=5)
    geom = models.MultiPolygonField(srid=4326)

    region = models.OneToOneField("Region", on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=40)
    nuts = models.CharField(max_length=5)
    geom = models.MultiPolygonField(srid=4326)

    region = models.OneToOneField("Region", on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    def __str__(self):
        return self.name


class District(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50)
    area = models.FloatField()
    population = models.BigIntegerField()
    hospitals = models.IntegerField()
    den_p_h_km = models.FloatField(null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "type", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_file = "AdminAreas"
    mapping = {
        "name": "DISTRICT",
        "area": "Shape__Are",
        "geom": "MULTIPOLYGON",
        "population": "pop_2020",
        "hospitals": "NUM_hosp",
        "den_p_h_km": "den_p_h_km",
    }

    def __str__(self):
        return self.name


class Municipality(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ags = models.CharField(max_length=8)
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=40)
    nuts = models.CharField(max_length=5)
    district_id = models.BigIntegerField()
    geom = models.MultiPolygonField(srid=4326)

    region = models.OneToOneField("Region", on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    def __str__(self):
        return self.name


class Grid(models.Model):
    geom = models.MultiLineStringField(srid=4326)
    source = models.CharField(max_length=100)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "type", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_file = "Electricity_Infrastructure"
    layer = "GridNetwork"
    mapping = {
        "source": "source",
        "geom": "MULTILINESTRING",
    }

    def __str__(self):
        return self.source
