import json
import os
import pathlib
from collections import namedtuple

from django.conf import settings
from range_key_dict import RangeKeyDict

from egon import __version__

# FILES
MAP_DIR = settings.APPS_DIR.path("map")
POPUPS_DIR = MAP_DIR.path("popups")

CLUSTER_GEOJSON_FILE = settings.DATA_DIR.path("cluster.geojson")
LAYER_STYLES_FILE = os.path.join(os.path.dirname(__file__), "../static/styles/layer_styles.json")

# REGIONS

MIN_ZOOM = 5
MAX_ZOOM = 22
MAX_DISTILLED_ZOOM = 10
DEFAULT_CLUSTER_ZOOM = 11

Zoom = namedtuple("MinMax", ["min", "max"])
ZOOM_LEVELS = {
    "country": Zoom(MIN_ZOOM, 6),
    "state": Zoom(6, 8),
    "district": Zoom(8, 10),
    "municipality": Zoom(10, MAX_ZOOM + 1),
}
REGIONS = (
    "country",
    "state",
    "district",
    "municipality",
)
REGION_ZOOMS = RangeKeyDict({zoom: layer for layer, zoom in ZOOM_LEVELS.items() if layer in REGIONS})


# FILTERS

FILTER_DEFINITION = {}


# STORE

STORE_COLD_INIT = {
    "version": __version__,
}


def init_hot_store():
    # Filter booleans have to be stored as str:
    filter_init = {}
    for _, data in FILTER_DEFINITION.items():
        initial = data["initial"]
        if initial is True:
            initial = "True"
        elif initial is False:
            initial = "False"
        filter_init[data["js_event_name"]] = initial
    return json.dumps(filter_init)


STORE_HOT_INIT = init_hot_store()


# SOURCES


def init_sources():
    sources = {}
    metadata_path = pathlib.Path(settings.METADATA_DIR)
    for metafile in [_ for _ in metadata_path.iterdir() if _.suffix == ".json"]:
        with open(metafile, "r", encoding="utf-8") as metadata_raw:
            metadata = json.loads(metadata_raw.read())
            sources[metadata["id"]] = metadata
    return sources


SOURCES = init_sources()


# STYLES

with open(
    LAYER_STYLES_FILE,
    mode="rb",
) as f:
    LAYER_STYLES = json.loads(f.read())


# DISTILL

# Tiles of Ghana: At z=5 Ghana has width x=15-16 and height y=15(-16)
X_AT_MIN_Z = 15
Y_AT_MIN_Z = 15
X_OFFSET = 1
Y_OFFSET = 0


def get_tile_coordinates_for_region(region):
    for z in range(MIN_ZOOM, MAX_DISTILLED_ZOOM + 1):
        z_factor = 2 ** (z - MIN_ZOOM)
        for x in range(X_AT_MIN_Z * z_factor, (X_AT_MIN_Z + 1) * z_factor + X_OFFSET):
            for y in range(Y_AT_MIN_Z * z_factor, (Y_AT_MIN_Z + 1) * z_factor + Y_OFFSET):
                if region in REGIONS and REGION_ZOOMS[z] != region:
                    continue
                yield x, y, z
