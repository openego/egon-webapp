from dataclasses import dataclass
from enum import Enum

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

from egon.map.managers import LabelMVTManager, RegionMVTManager


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
            ("flexibility", _("Flexibility")),
        ],
        default="demand",
        help_text="The main category in the left panel in the frontend.",
    )
    sub_category = models.CharField(
        max_length=64, null=True, blank=True, help_text="The sub-category for the display in the frontend."
    )
    order_priority = models.PositiveSmallIntegerField(
        verbose_name=_("Order priority Frontend"),
        null=True,
        blank=True,
        help_text=_(
            "The MapLayers in the frontend-panel on the left are ordered by their category, then sub-category "
            "and finally by this field. '1' is the highest priority."
        ),
    )
    data_model = models.CharField(max_length=64, help_text="The name of the model that holds the data.")

    data_file = "maplayer"

    def __str__(self):
        return self.get_category_display() + ": " + self.name + " (" + self.scenario + ")"

    class Meta:
        verbose_name = _("Map Layer")
        verbose_name_plural = _("Map Layers")
