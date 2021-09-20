import json
import os
from dataclasses import dataclass, field
from itertools import product
from typing import List, Optional

from django.db.models import IntegerField, BooleanField, Model
from django.utils.translation import gettext_lazy as _
from raster.models import RasterLayer as RasterModel

from config.settings.base import USE_DISTILLED_MVTS
from .config import MAX_ZOOM, MIN_ZOOM, REGIONS, ZOOM_LEVELS, MAX_DISTILLED_ZOOM, LAYER_STYLES

from . import models

with open(os.path.join(os.path.dirname(__file__), "../static/styles/layer_styles.json"), mode="rb",) as f:
    LAYER_STYLES = json.loads(f.read())


def get_color(source_layer):
    return LAYER_STYLES[source_layer]["paint"]["fill-color"]


def get_opacity(source_layer):
    return LAYER_STYLES[source_layer]["paint"]["fill-opacity"]


@dataclass
class VectorLayerData:
    source: str
    color: str
    model: Model.__class__
    name: str
    name_singular: str
    description: str
    popup_fields: list = field(default_factory=list)


@dataclass
class RasterLayerData:
    source: str
    filepath: str
    legend: str
    model: RasterModel.__class__
    name: str
    name_singular: str
    description: str


DEMAND: list = [
    VectorLayerData(
        source="demand_cts",
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
        popup_fields=["id", "demand"]
    ),
]

GENERATION: list = [
    VectorLayerData(
        source="supply_biomass",
        color="blue",
        model=models.SupplyBiomass,
        name=_("Biomasse"),
        name_singular=_("Biomasse"),
        description=_("Text einfügen"),
        popup_fields=["id", "carrier"],
    ),
    VectorLayerData(
        source="supply_run_of_river",
        color="blue",
        model=models.SupplyRunOfRiver,
        name=_("Hydro"),
        name_singular=_("Hydro"),
        description=_("Text einfügen"),
        popup_fields=["id", "carrier"],
    ),
    VectorLayerData(
        source="supply_wind",
        color="blue",
        model=models.SupplyWindOnshore,
        name=_("Wind onshore"),
        name_singular=_("Wind onshore"),
        description=_("Text einfügen"),
        popup_fields=["id", "carrier"],
    ),
    VectorLayerData(
        source="supply_solar",
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
        color="blue",
        model=models.EHVLine,
        name=_("EHV Leitung"),
        name_singular=_("EHV Leitung"),
        description=_("Text einfügen"),
    ),
    VectorLayerData(
        source="hv_line",
        color="darkblue",
        model=models.HVLine,
        name=_("HV Leitung"),
        name_singular=_("HV Leitung"),
        description=_("Text einfügen"),
    ),
    VectorLayerData(
        source="ehv_hv_station",
        color="green",
        model=models.EHVHVSubstation,
        name=_("EHV/HV Substation"),
        name_singular=_("EHV/HV Substation"),
        description=_("Text einfügen"),
    ),
    VectorLayerData(
        source="hv_mv_station",
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
        color="pink",
        model=models.MVGridDistricts,
        name=_("MV Grid Districts"),
        name_singular=_("MV Grid Districts"),
        description=_("Text einfügen"),
    ),
]

LAYERS_DEFINITION: list = DEMAND + GENERATION + GRID + MODEL
LAYERS_CATEGORIES: dict = {
    "demand": DEMAND,
    "generation": GENERATION,
    "grid": GRID,
    "model": MODEL
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


def get_raster_sources(distilled=False):
    sources = []
    for layer in LAYERS_DEFINITION:
        if not issubclass(layer.model, RasterModel):
            continue
        try:
            raster_id = RasterModel.objects.get(name=layer.source).id
        except ObjectDoesNotExist:
            continue
        sources.append(
            Source(
                name=f"{layer.source}",
                type="raster",
                tiles=[f"raster/tiles/{raster_id}/{{z}}/{{x}}/{{y}}.png?legend={layer.legend}"],
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
            Source(name=region, type="vector", tiles=[f"static/mvts/{{z}}/{{x}}/{{y}}/{region}.mvt"],)
            for region in REGIONS
            if ZOOM_LEVELS[region].min < MAX_DISTILLED_ZOOM
        ]
        + [
            Source(name="static", type="vector", tiles=["static_mvt/{z}/{x}/{y}/"]),
            Source(name="static_distilled", type="vector", tiles=["static/mvts/{z}/{x}/{y}/static.mvt"],),
        ]
        + get_raster_sources()
        + get_dynamic_sources()
    )
else:
    SUFFIXES = [""]
    ALL_SOURCES = (
        [Source(name=region, type="vector", tiles=[f"{region}_mvt/{{z}}/{{x}}/{{y}}/"]) for region in REGIONS]
        + [Source(name="static", type="vector", tiles=["static_mvt/{z}/{x}/{y}/"])]
        + get_raster_sources()
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

RASTER_LAYERS = [
    RasterLayer(id=layer.source, source=layer.source, type="raster",)
    for layer in LAYERS_DEFINITION
    if issubclass(layer.model, RasterModel)
]

POPUPS = []
STATIC_LAYERS = []
for layer in LAYERS_DEFINITION:
    if issubclass(layer.model, RasterModel):
        continue
    if hasattr(layer.model, "setup"):
        continue
    for suffix in SUFFIXES:
        layer_id = f"fill-{layer.source}{suffix}"
        STATIC_LAYERS.append(
            Layer(
                id=layer_id,
                color=layer.color,
                description=layer.description,
                minzoom=MAX_DISTILLED_ZOOM + 1 if suffix == "" and USE_DISTILLED_MVTS else MIN_ZOOM,
                maxzoom=MAX_ZOOM if suffix == "" else MAX_DISTILLED_ZOOM + 1,
                name=layer.name,
                style=layer.source,
                source=f"static{suffix}",
                source_layer=layer.source,
                type="static",
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
