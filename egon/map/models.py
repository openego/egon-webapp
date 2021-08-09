from django.contrib.gis.db import models
from .managers import RegionMVTManager, LabelMVTManager, MVTManager, CenterMVTManager


# REGIONS


class Region(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_file = "Gha_AdminBoundaries"
    layer = "Gha_Regions_01"
    mapping = {
        "geom": "MULTIPOLYGON",
        "name": "Region",
    }

    def __str__(self):
        return self.name


class District(models.Model):
    geom = models.MultiPolygonField(srid=4326)
    name = models.CharField(max_length=50, unique=True)
    area = models.FloatField()
    population = models.BigIntegerField()

    region = models.ForeignKey("Region", on_delete=models.CASCADE, related_name="districts")

    objects = models.Manager()
    vector_tiles = RegionMVTManager(columns=["id", "name", "bbox"])
    label_tiles = LabelMVTManager(geo_col="geom_label", columns=["id", "name"])

    data_file = "Gha_AdminBoundaries"
    layer = "Gha_Districts_02"
    mapping = {
        "geom": "MULTIPOLYGON",
        "name": "District",
        "area": "Area_km2",
        "population": "Pop2020",
        "region": {"name": "Region"},  # ForeignKey see https://stackoverflow.com/a/46689928/5804947
    }

    def __str__(self):
        return self.name


# LAYER
