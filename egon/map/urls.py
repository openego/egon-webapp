from django.conf import settings
from django.urls import path
from django_distill import distill_path
from djgeojson.views import GeoJSONLayerView

from egon.map.mapset.mvt_layers import DISTILL_MVT_LAYERS, MVT_LAYERS

from . import views
from .config import get_tile_coordinates_for_region
from .mvt import mvt_view_factory
from .mapset import setup

app_name = "map"

urlpatterns = [
    path("", views.MapGLView.as_view(), name="map"),
    path("clusters", views.get_clusters, name="clusters"),
]

urlpatterns += [
    path(f"clusters/{name}.geojson", GeoJSONLayerView.as_view(model=cluster_layer.model))
    for name, cluster_layer in setup.STATIC_LAYERS.items()
]

urlpatterns += [
    path(name + "_mvt/<int:z>/<int:x>/<int:y>/", mvt_view_factory(name, layers)) for name, layers in MVT_LAYERS.items()
]


def get_all_statics_for_state_lod(view_name):
    for x, y, z in get_tile_coordinates_for_region(view_name):
        yield z, x, y


# Distill MVT-urls:
if settings.DISTILL:
    urlpatterns += [
        distill_path(
            f"<int:z>/<int:x>/<int:y>/{name}.mvt",
            mvt_view_factory(name, layers),
            name=name,
            distill_func=get_all_statics_for_state_lod,
            distill_status_codes=(200, 204, 400),
        )
        for name, layers in DISTILL_MVT_LAYERS.items()
    ]
