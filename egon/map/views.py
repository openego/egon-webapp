import json

from django.conf import settings
from django.http import HttpRequest, response
from django.views.generic import TemplateView
from django_mapengine import views

from config.settings.base import PASSWORD, PASSWORD_PROTECTION

from . import map_config
from .config import SOURCES, STORE_COLD_INIT, STORE_HOT_INIT
from .forms import StaticLayerForm
from .models import TransportMitDemand


class MapGLView(TemplateView, views.MapEngineMixin):
    template_name = "map.html"
    extra_context = {
        "password_protected": PASSWORD_PROTECTION,
        "password": PASSWORD,
        "area_switches": {
            category: [StaticLayerForm(layer) for layer in layers] for category, layers in map_config.LEGEND.items()
        },
        "store_hot_init": STORE_HOT_INIT,
    }

    def get_context_data(self, **kwargs):
        # Add unique session ID
        context = super().get_context_data(**kwargs)

        # Categorize sources
        categorized_sources = {
            category: [SOURCES[layer.get_layer_id()] for layer in layers if layer.get_layer_id() in SOURCES]
            for category, layers in map_config.LEGEND.items()
        }
        context["sources"] = categorized_sources

        context["store_cold_init"] = json.dumps(STORE_COLD_INIT)

        return context


# pylint: disable=W0613
def get_choropleth(request: HttpRequest, lookup: str, scenario: str) -> response.JsonResponse:  # noqa: ARG001
    """Read scenario results from database, aggregate data and send back data.

    Parameters
    ----------
    request : HttpRequest
        Request can contain optional values (i.e. language)
    lookup : str
        which result/calculation shall be shown in choropleth?
    scenario : str
        defines the scenario to look up values for (i.e. status quo or user scenario)

    Returns
    -------
    JsonResponse
        Containing key-value pairs of municipality_ids and values and related color style
    """
    queryset = TransportMitDemand.objects.values("mv_grid_district", "demand")
    values = {val["mv_grid_district"]: val["demand"] for val in queryset}
    fill_color = settings.MAP_ENGINE_CHOROPLETH_STYLES.get_fill_color(lookup, list(values.values()))
    return response.JsonResponse({"values": values, "paintProperties": {"fill-color": fill_color, "fill-opacity": 0.7}})
