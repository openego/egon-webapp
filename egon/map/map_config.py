"""Actual map setup is done here."""

from dataclasses import dataclass
from typing import Optional

from django.conf import settings

from egon.map import models
from egon.map import config
from django_mapengine import layers, utils, sources, mvt

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

if settings.MAP_ENGINE_USE_DISTILLED_MVTS:
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
    sources.MapSource(
        "satellite",
        type="raster",
        tiles=[
            "https://api.maptiler.com/tiles/satellite-v2/"
            f"{{z}}/{{x}}/{{y}}.jpg?key={settings.MAP_ENGINE_TILING_SERVICE_TOKEN}",
        ],
    ),
    sources.ClusterMapSource("supply_biomass", type="geojson", url="clusters/supply_biomass.geojson"),
    sources.MapSource(name="static", type="vector", tiles=["static_mvt/{z}/{x}/{y}/"]),
    sources.MapSource(name="static_distilled", type="vector", tiles=["static/mvts/{z}/{x}/{y}/static.mvt"]),
    sources.MapSource(name="results", type="vector", tiles=["results_mvt/{z}/{x}/{y}/"]),
]


REGION_MVT_LAYERS = {
    "country": [
        mvt.MVTLayer("country", models.Country.vector_tiles),
        mvt.MVTLayer("countrylabel", models.Country.label_tiles),
    ],
    "state": [
        mvt.MVTLayer("state", models.State.vector_tiles),
        mvt.MVTLayer("statelabel", models.State.label_tiles),
    ],
    "district": [
        mvt.MVTLayer("district", models.District.vector_tiles),
        mvt.MVTLayer("districtlabel", models.District.label_tiles),
    ],
    "municipality": [
        mvt.MVTLayer("municipality", models.Municipality.vector_tiles),
        mvt.MVTLayer("municipalitylabel", models.Municipality.label_tiles),
    ],
}

STATIC_MVT_LAYERS = {
    "static": [
        mvt.MVTLayer("demand_cts", models.DemandCts.vector_tiles),
        mvt.MVTLayer("demand_household", models.DemandHousehold.vector_tiles),
        mvt.MVTLayer("supply_biomass", models.SupplyBiomass.vector_tiles),
        mvt.MVTLayer("supply_run_of_river", models.SupplyRunOfRiver.vector_tiles),
        mvt.MVTLayer("supply_wind", models.SupplyWindOnshore.vector_tiles),
        mvt.MVTLayer("supply_solar", models.SupplySolarGround.vector_tiles),
        mvt.MVTLayer("potential_wind", models.SupplyPotentialWind.vector_tiles),
        mvt.MVTLayer("potential_pv", models.SupplyPotentialPVGround.vector_tiles),
        mvt.MVTLayer("ehv_line", models.EHVLine.vector_tiles),
        mvt.MVTLayer("hv_line", models.HVLine.vector_tiles),
        mvt.MVTLayer("ehv_hv_station", models.EHVHVSubstation.vector_tiles),
        mvt.MVTLayer("hv_mv_station", models.HVMVSubstation.vector_tiles),
        mvt.MVTLayer("mv_grid_districts", models.MVGridDistricts.vector_tiles),
    ]
}

DYNAMIC_MVT_LAYERS = {}

MVT_LAYERS = dict(**REGION_MVT_LAYERS, **STATIC_MVT_LAYERS, **DYNAMIC_MVT_LAYERS)
DISTILL_MVT_LAYERS = dict(**REGION_MVT_LAYERS, **STATIC_MVT_LAYERS)
