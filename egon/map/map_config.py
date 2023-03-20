"""Actual map setup is done here."""

from dataclasses import dataclass
from typing import Optional

from django.conf import settings
from django_mapengine import layers, mvt, sources, utils

from egon.map import config, models

STATIC_LAYERS = {
    "supply_biomass": layers.ClusterModelLayer(
        id="supply_biomass", model=models.SupplyBiomass, type="symbol", source="supply_biomass"
    ),
    "supply_run_of_river": layers.ClusterModelLayer(
        id="supply_run_of_river", model=models.SupplyRunOfRiver, type="symbol", source="supply_run_of_river"
    ),
    "supply_wind": layers.ClusterModelLayer(
        id="supply_wind", model=models.SupplyWindOnshore, type="symbol", source="supply_wind"
    ),
    "supply_solar": layers.ClusterModelLayer(
        id="supply_solar", model=models.SupplySolarGround, type="symbol", source="supply_solar"
    ),
    "potential_wind": layers.StaticModelLayer(
        id="potential_wind", model=models.SupplyPotentialWind, type="fill", source="static"
    ),
    "potential_pv": layers.StaticModelLayer(
        id="potential_pv", model=models.SupplyPotentialPVGround, type="fill", source="static"
    ),
    "ehv_line": layers.StaticModelLayer(id="ehv_line", model=models.EHVLine, type="line", source="static"),
    "hv_line": layers.StaticModelLayer(id="hv_line", model=models.HVLine, type="line", source="static"),
    "ehv_hv_station": layers.ClusterModelLayer(
        id="ehv_hv_station", model=models.EHVHVSubstation, type="symbol", source="ehv_hv_station"
    ),
    "hv_mv_station": layers.ClusterModelLayer(
        id="hv_mv_station", model=models.HVMVSubstation, type="symbol", source="hv_mv_station"
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
    "generation": [
        LegendLayer("Biomasse", "", STATIC_LAYERS["supply_biomass"]),
        LegendLayer("Hydro", "", STATIC_LAYERS["supply_run_of_river"]),
        LegendLayer("Wind Onshore", "", STATIC_LAYERS["supply_wind"]),
        LegendLayer("Solar", "", STATIC_LAYERS["supply_solar"]),
        LegendLayer("Potential Wind", "", STATIC_LAYERS["potential_wind"]),
        LegendLayer("Potential PV", "", STATIC_LAYERS["potential_pv"]),
    ],
    "grid": [
        LegendLayer("EHV Line", "", STATIC_LAYERS["ehv_line"]),
        LegendLayer("HV Line", "", STATIC_LAYERS["hv_line"]),
        LegendLayer("EHV/HV Stations", "", STATIC_LAYERS["ehv_hv_station"]),
        LegendLayer("HV/MV Stations", "", STATIC_LAYERS["hv_mv_station"]),
    ],
}

REGION_LAYERS = list(layers.get_region_layers())
RESULT_LAYERS = []


# Order is important! Last items are shown on top!
ALL_LAYERS = REGION_LAYERS + RESULT_LAYERS
for static_layer in STATIC_LAYERS.values():
    ALL_LAYERS.extend(static_layer.get_map_layers())

LAYERS_AT_STARTUP = [layer.id for layer in REGION_LAYERS]

POPUPS = ["results"]

if settings.MAP_ENGINE_USE_DISTILLED_MVTS:
    SOURCES = [
        sources.MapSource(name=region, type="vector", tiles=[f"map/{region}_mvt/{{z}}/{{x}}/{{y}}/"])
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
        sources.MapSource(name=region, type="vector", tiles=[f"map/{region}_mvt/{{z}}/{{x}}/{{y}}/"])
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
    sources.ClusterMapSource("supply_biomass", type="geojson", url="map/clusters/supply_biomass.geojson"),
    sources.ClusterMapSource("supply_run_of_river", type="geojson", url="map/clusters/supply_run_of_river.geojson"),
    sources.ClusterMapSource("supply_wind", type="geojson", url="map/clusters/supply_wind.geojson"),
    sources.ClusterMapSource("supply_solar", type="geojson", url="map/clusters/supply_solar.geojson"),
    sources.ClusterMapSource("ehv_hv_station", type="geojson", url="map/clusters/ehv_hv_station.geojson"),
    sources.ClusterMapSource("hv_mv_station", type="geojson", url="map/clusters/hv_mv_station.geojson"),
    sources.MapSource(name="static", type="vector", tiles=["map/static_mvt/{z}/{x}/{y}/"]),
    sources.MapSource(name="static_distilled", type="vector", tiles=["static/mvts/{z}/{x}/{y}/static.mvt"]),
    sources.MapSource(name="results", type="vector", tiles=["map/results_mvt/{z}/{x}/{y}/"]),
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
        mvt.MVTLayer("potential_wind", models.SupplyPotentialWind.vector_tiles),
        mvt.MVTLayer("potential_pv", models.SupplyPotentialPVGround.vector_tiles),
        mvt.MVTLayer("ehv_hv_station", models.EHVHVSubstation.vector_tiles),
        mvt.MVTLayer("hv_mv_station", models.HVMVSubstation.vector_tiles),
        mvt.MVTLayer("mv_grid_districts", models.MVGridDistricts.vector_tiles),
    ]
}

DYNAMIC_MVT_LAYERS = {}

MVT_LAYERS = {**REGION_MVT_LAYERS, **STATIC_MVT_LAYERS, **DYNAMIC_MVT_LAYERS}
DISTILL_MVT_LAYERS = {**REGION_MVT_LAYERS, **STATIC_MVT_LAYERS}
