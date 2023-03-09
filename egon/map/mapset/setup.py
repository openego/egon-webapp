"""Actual map setup is done here."""

from dataclasses import dataclass
from typing import Optional

from django.conf import settings

from .. import models
from .. import config
from . import layers, sources, utils

STATIC_LAYERS = {
    "supply_biomass": layers.ClusterModelLayer(
        id="supply_biomass", model=models.SupplyBiomass, type="symbol", source="supply_biomass"
    ),
}


@dataclass
class LegendLayer:
    """Define a legend item with color which can activate a layer from model in map."""

    name: str
    description: str
    layer: layers.ModelLayer
    color: Optional[str] = None

    def get_color(self) -> str:
        """
        Return color to show on legend. If color is not set, color is tried to be read from layer style.

        Returns
        -------
        str
            Color string (name/rgb/hex/etc.) to be used on legend in frontend.
        """
        if self.color:
            return self.color
        return utils.get_color(self.layer.id)


LEGEND = {
    "Demand": [
        LegendLayer("Biomasse", "", STATIC_LAYERS["supply_biomass"]),
    ],
}

REGION_LAYERS = layers.get_region_layers()
RESULT_LAYERS = []


# Order is important! Last items are shown on top!
ALL_LAYERS = REGION_LAYERS + RESULT_LAYERS
for static_layer in STATIC_LAYERS.values():
    ALL_LAYERS.extend(static_layer.get_map_layers())

LAYERS_AT_STARTUP = [layer.id for layer in REGION_LAYERS]

POPUPS = ["results"]

if settings.USE_DISTILLED_MVTS:
    SOURCES = [
        sources.MapSource(name=region, type="vector", tiles=[f"{region}_mvt/{{z}}/{{x}}/{{y}}/"])
        for region in config.REGIONS
        if config.ZOOM_LEVELS[region].min > config.MAX_DISTILLED_ZOOM
    ] + [
        sources.MapSource(
            name=region,
            type="vector",
            tiles=[f"static/mvts/{{z}}/{{x}}/{{y}}/{region}.mvt"],
            maxzoom=config.MAX_DISTILLED_ZOOM + 1,
        )
        for region in config.REGIONS
        if config.ZOOM_LEVELS[region].min < config.MAX_DISTILLED_ZOOM
    ]
else:
    SOURCES = [
        sources.MapSource(name=region, type="vector", tiles=[f"{region}_mvt/{{z}}/{{x}}/{{y}}/"])
        for region in config.REGIONS
    ]

SOURCES += [
    sources.ClusterMapSource("supply_biomass", type="geojson", url="clusters/supply_biomass.geojson"),
    sources.MapSource(name="static", type="vector", tiles=["static_mvt/{z}/{x}/{y}/"]),
    sources.MapSource(name="static_distilled", type="vector", tiles=["static/mvts/{z}/{x}/{y}/static.mvt"]),
    sources.MapSource(name="results", type="vector", tiles=["results_mvt/{z}/{x}/{y}/"]),
]
