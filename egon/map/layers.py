import json
from dataclasses import dataclass, field
from itertools import product
from enum import Enum
from typing import List, Optional

from django.db.models import IntegerField, BooleanField, Model
from django.utils.translation import gettext_lazy as _

from config.settings.base import USE_DISTILLED_MVTS
from .config import MAX_ZOOM, MIN_ZOOM, REGIONS, ZOOM_LEVELS, MAX_DISTILLED_ZOOM, LAYER_STYLES

from . import models


def get_color(source_layer):
    return LAYER_STYLES[source_layer]["paint"]["fill-color"]


def get_opacity(source_layer):
    return LAYER_STYLES[source_layer]["paint"]["fill-opacity"]


def get_choropleth_colors_for_legend(source_layer):
    fill_color = get_color(source_layer)
    colors = fill_color[2::2]
    values = fill_color[3::2]
    ranges = []
    for i, value in enumerate(values):
        if i == 0:
            ranges.append(f"0 - {value}")
        else:
            ranges.append(f"{values[i-1]} - {value}")
    return list(zip(ranges, colors))


class LayerType(Enum):
    Fill = 0
    Symbol = 1
    Line = 2
    Choropleth = 3
    Raster = 4


@dataclass
class VectorLayerData:
    source: str
    color: str
    model: Model.__class__
    name: str
    name_singular: str
    description: str
    clustered: bool = False
    type: LayerType = LayerType.Fill
    popup_fields: list = field(default_factory=list)


DEMAND: list = [
    VectorLayerData(
        source="demand_cts",
        type=LayerType.Choropleth,
        color=get_color("demand_cts"),
        model=models.DemandCts,
        name=_("Cts"),
        name_singular=_("Ct"),
        description=_(
            "Mit dem Schalter blenden Sie die Siedlungsflächen mit dem gewählten Abstand zu Siedlungen in der Karte "
            "ein und aus. Nur mit dem Regler unter 'Mein Szenario' können Sie festlegen, welcher Abstand von "
            "Siedlungen zu Windenergieanlagen eingehalten werden soll, um die Windpotenzialflächen zu ermitteln.<br>"
            "<br>Eine Siedlung ist ein Gebiet, welches die menschliche Niederlassung in beliebiger Form der "
            "gruppierten Behausung beschreibt. Sie beinhaltet überwiegend Wohngebiete."
        ),
    ),
    VectorLayerData(
        source="demand_household",
        type=LayerType.Choropleth,
        color="#fd8d3c",
        model=models.DemandHousehold,
        name=_("Haushalte"),
        name_singular=_("Haushalt"),
        description=_(
            "Mit dem Schalter blenden Sie die Siedlungsflächen mit dem gewählten Abstand zu Siedlungen in der Karte "
            "ein und aus. Nur mit dem Regler unter 'Mein Szenario' können Sie festlegen, welcher Abstand von "
            "Siedlungen zu Windenergieanlagen eingehalten werden soll, um die Windpotenzialflächen zu ermitteln.<br>"
            "<br>Eine Siedlung ist ein Gebiet, welches die menschliche Niederlassung in beliebiger Form der "
            "gruppierten Behausung beschreibt. Sie beinhaltet überwiegend Wohngebiete."
        ),
        popup_fields=["id", "demand"],
    ),
]

GENERATION: list = [
    VectorLayerData(
        source="supply_biomass",
        type=LayerType.Symbol,
        color="blue",
        model=models.SupplyBiomass,
        name=_("Biomasse"),
        name_singular=_("Biomasse"),
        description=_("Text einfügen"),
        clustered=True,
        popup_fields=["id", "carrier"],
    ),
    VectorLayerData(
        source="supply_run_of_river",
        type=LayerType.Symbol,
        color="blue",
        model=models.SupplyRunOfRiver,
        name=_("Hydro"),
        name_singular=_("Hydro"),
        description=_("Text einfügen"),
        popup_fields=["id", "carrier"],
    ),
    VectorLayerData(
        source="supply_wind",
        type=LayerType.Symbol,
        color="blue",
        model=models.SupplyWindOnshore,
        name=_("Wind onshore"),
        name_singular=_("Wind onshore"),
        description=_("Text einfügen"),
        popup_fields=["id", "carrier"],
    ),
    VectorLayerData(
        source="supply_solar",
        type=LayerType.Symbol,
        color="yellow",
        model=models.SupplySolarGround,
        name=_("Solar"),
        name_singular=_("Solar"),
        description=_("Text einfügen"),
        popup_fields=["id", "carrier"],
    ),
    VectorLayerData(
        source="potential_wind",
        color=get_color("potential_wind"),
        model=models.SupplyPotentialWind,
        name=_("Windpotenzial"),
        name_singular=_("Windpotenzial"),
        description=_("Text einfügen"),
    ),
    VectorLayerData(
        source="potential_pv",
        color=get_color("potential_pv"),
        model=models.SupplyPotentialPVGround,
        name=_("PV-Potenzial"),
        name_singular=_("PV-Potenzial"),
        description=_("Text einfügen"),
    ),
]

GRID: list = [
    VectorLayerData(
        source="ehv_line",
        type=LayerType.Line,
        color="blue",
        model=models.EHVLine,
        name=_("EHV Leitung"),
        name_singular=_("EHV Leitung"),
        description=_("Text einfügen"),
    ),
    VectorLayerData(
        source="hv_line",
        type=LayerType.Line,
        color="darkblue",
        model=models.HVLine,
        name=_("HV Leitung"),
        name_singular=_("HV Leitung"),
        description=_("Text einfügen"),
    ),
    VectorLayerData(
        source="ehv_hv_station",
        type=LayerType.Symbol,
        color="green",
        model=models.EHVHVSubstation,
        name=_("EHV/HV Substation"),
        name_singular=_("EHV/HV Substation"),
        description=_("Text einfügen"),
    ),
    VectorLayerData(
        source="hv_mv_station",
        type=LayerType.Symbol,
        color="blue",
        model=models.HVMVSubstation,
        name=_("HV/MV Substation"),
        name_singular=_("HV/MV Substation"),
        description=_("Text einfügen"),
    ),
]

MODEL: list = [
    VectorLayerData(
        source="mv_grid_districts",
        type=LayerType.Choropleth,
        color="pink",
        model=models.MVGridDistricts,
        name=_("MV Grid Districts"),
        name_singular=_("MV Grid Districts"),
        description=_("Text einfügen"),
    ),
]

LAYERS_DEFINITION: list = DEMAND + GENERATION + GRID + MODEL
LAYERS_CATEGORIES: dict = {"demand": DEMAND, "generation": GENERATION, "grid": GRID, "model": MODEL}


CHOROPLETH_LAYERS = {
    "demand_cts": {"title": "CTs [MWh]", "colors": get_choropleth_colors_for_legend("demand_cts")},
    "demand_household": {"title": "Haushalte [MWh]", "colors": get_choropleth_colors_for_legend("demand_household")},
    "mv_grid_districts": {
        "title": "Grid Districts [MV]",
        "colors": get_choropleth_colors_for_legend("mv_grid_districts"),
    },
}


@dataclass
class Source:
    name: str
    type: str
    tiles: Optional[List[str]] = None
    url: Optional[str] = None


@dataclass
class Layer:
    id: str
    minzoom: int
    maxzoom: int
    style: str
    source: str
    source_layer: str
    type: str
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    clustered: bool = False
    style_type: Optional[LayerType] = None


@dataclass
class RasterLayer:
    id: str
    source: str
    type: str


@dataclass
class Popup:
    source: str
    layer_id: str
    fields: str


def get_layer_setups(layer):
    setups = []
    setup_model = layer["model"]._meta.get_field("setup").related_model
    for setup in setup_model._meta.fields:
        if setup.name == "id":
            continue
        if isinstance(setup, IntegerField):
            setups.append([f"{setup.name}={choice[0]}" for choice in setup.choices])
        elif isinstance(setup, BooleanField):
            setups.append([f"{setup.name}=True", f"{setup.name}=False"])
    return product(*setups)


def get_dynamic_sources():
    sources = []
    for layer in LAYERS_DEFINITION:
        if not hasattr(layer.model, "setup"):
            continue
        for combination in get_layer_setups(layer):
            mvt_str = "-".join(combination)
            filter_str = "&".join(map(lambda x: f"setup__{x}", combination))
            sources.append(
                Source(
                    name=f"{layer.source}-{mvt_str}",
                    type="vector",
                    tiles=[f"{layer.source}_mvt/{{z}}/{{x}}/{{y}}/?{filter_str}"],
                )
            )
    return sources


if USE_DISTILLED_MVTS:
    SUFFIXES = ["", "_distilled"]
    ALL_SOURCES = (
        [
            Source(name=region, type="vector", tiles=[f"{region}_mvt/{{z}}/{{x}}/{{y}}/"])
            for region in REGIONS
            if ZOOM_LEVELS[region].min > MAX_DISTILLED_ZOOM
        ]
        + [
            Source(
                name=region,
                type="vector",
                tiles=[f"static/mvts/{{z}}/{{x}}/{{y}}/{region}.mvt"],
            )
            for region in REGIONS
            if ZOOM_LEVELS[region].min < MAX_DISTILLED_ZOOM
        ]
        + [
            Source(name="static", type="vector", tiles=["static_mvt/{z}/{x}/{y}/"]),
            Source(
                name="static_distilled",
                type="vector",
                tiles=["static/mvts/{z}/{x}/{y}/static.mvt"],
            ),
        ]
        + get_dynamic_sources()
    )
else:
    SUFFIXES = [""]
    ALL_SOURCES = (
        [Source(name=region, type="vector", tiles=[f"{region}_mvt/{{z}}/{{x}}/{{y}}/"]) for region in REGIONS]
        + [Source(name="static", type="vector", tiles=["static_mvt/{z}/{x}/{y}/"])]
        + get_dynamic_sources()
    )

REGION_LAYERS = (
    [
        Layer(
            id=f"line-{layer}",
            minzoom=ZOOM_LEVELS[layer].min,
            maxzoom=ZOOM_LEVELS[layer].max,
            style="region-line",
            source=layer,
            source_layer=layer,
            type="region",
        )
        for layer in REGIONS
    ]
    + [
        Layer(
            id=f"fill-{layer}",
            minzoom=ZOOM_LEVELS[layer].min,
            maxzoom=ZOOM_LEVELS[layer].max,
            style="region-fill",
            source=layer,
            source_layer=layer,
            type="region",
        )
        for layer in REGIONS
    ]
    + [
        Layer(
            id=f"label-{layer}",
            maxzoom=ZOOM_LEVELS[layer].max,
            minzoom=ZOOM_LEVELS[layer].min,
            style="region-label",
            source=layer,
            source_layer=f"{layer}label",
            type="region",
        )
        for layer in REGIONS
    ]
)

POPUPS = []
STATIC_LAYERS = []
for layer in LAYERS_DEFINITION:
    if hasattr(layer.model, "setup"):
        continue
    for suffix in SUFFIXES:
        if layer.clustered and suffix == "_distilled":
            # Clustered layers are not distilled
            continue
        layer_id = f"{layer.source}{suffix}"
        if layer.clustered:
            min_zoom = list(ZOOM_LEVELS.values())[-1].min  # Show unclustered only at last LOD
            max_zoom = MAX_ZOOM
        else:
            min_zoom = MAX_DISTILLED_ZOOM + 1 if suffix == "" and USE_DISTILLED_MVTS else MIN_ZOOM
            max_zoom = MAX_ZOOM if suffix == "" else MAX_DISTILLED_ZOOM + 1
        STATIC_LAYERS.append(
            Layer(
                id=layer_id,
                color=layer.color,
                description=layer.description,
                minzoom=min_zoom,
                maxzoom=max_zoom,
                name=layer.name,
                style=layer.source,
                style_type=layer.type,
                source=f"static{suffix}",
                source_layer=layer.source,
                type="static",
                clustered=layer.clustered,
            )
        )
        if layer.popup_fields:
            popup_fields = {}
            for popup_field in layer.popup_fields:
                label = (
                    getattr(layer.model, popup_field).field.verbose_name
                    if hasattr(layer.model, popup_field)
                    else popup_field
                )
                popup_fields[label] = popup_field
            POPUPS.append(Popup(layer.source, layer_id, json.dumps(popup_fields)))

# Sort popups according to prio:
POPUP_PRIO = ["hospital", "hospital_simulated"]  # from high to low prio
POPUPS = sorted(POPUPS, key=lambda x: len(POPUP_PRIO) if x.source not in POPUP_PRIO else POPUP_PRIO.index(x.source))

DYNAMIC_LAYERS = [
    Layer(
        id=f"fill-{layer.source}-{'-'.join(combination)}",
        color=layer.color,
        description=layer.description,
        minzoom=MIN_ZOOM,
        maxzoom=MAX_ZOOM,
        name=layer.name,
        style=layer.source,
        source=f"{layer.source}-{'-'.join(combination)}",
        source_layer=layer.source,
        type="static",
    )
    for layer in LAYERS_DEFINITION
    if hasattr(layer.model, "setup")
    for combination in get_layer_setups(layer)
]

ALL_LAYERS = STATIC_LAYERS + DYNAMIC_LAYERS + REGION_LAYERS
