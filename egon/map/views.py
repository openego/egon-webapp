import json

from django.conf import settings
from django.http import HttpRequest, response
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django_mapengine import views

from config.settings.base import PASSWORD, PASSWORD_PROTECTION

from . import map_config
from .config import SOURCES, STORE_COLD_INIT, STORE_HOT_INIT
from .forms import StaticLayerForm
from .models import DemandHousehold, MapLayer, MVGridDistrictData, TransportMitDemand


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


def get_popup(request: HttpRequest, lookup: str, region: int) -> response.JsonResponse:  # noqa: ARG001
    """Return popup as html and chart options to render chart on popup.

    Parameters
    ----------
    request : HttpRequest
        Request from app, can hold option for different language
    lookup: str
        Name is used to lookup data and chart functions
    region: int
        ID of region selected on map. Data and chart for popup is calculated for related region.

    Returns
    -------
    JsonResponse
        containing HTML to render popup and chart options to be used in E-Chart.
    """
    # data = calculations.create_data(lookup, region)
    if lookup in LOOKUPS:
        model = LOOKUPS[lookup]
        data = {"title": model._meta.verbose_name}
        raw_data = model.objects.filter(mv_grid_district=region).values(*model.popup_fields)[0]

        # Get the model's verbose field names
        verbose_field_names = {field.name: field.verbose_name for field in model._meta.get_fields()}
        # Replace field names in data with verbose names
        data_verbose = {}
        for field_name, value in raw_data.items():
            verbose_name = verbose_field_names.get(field_name, field_name)
            data_verbose[verbose_name] = value
        data["data"] = data_verbose
    else:
        map_layer = MapLayer.objects.get(layer_identifier=lookup)
        data = {"title": map_layer.popup_title, "description": map_layer.popup_description}
        raw_data = MVGridDistrictData.objects.filter(id=region).values(*map_layer.popup_fields)[0]

        # Get the model's verbose field names
        verbose_field_names = {field.name: field.verbose_name for field in MVGridDistrictData._meta.get_fields()}
        # Replace field names in data with verbose names
        data_verbose = {}
        for field_name, value in raw_data.items():
            verbose_name = verbose_field_names.get(field_name, field_name)
            if type(value) == float:
                value = round(value, 2)
            data_verbose[verbose_name] = value
        data["data"] = data_verbose

    try:
        html = render_to_string(f"popups/{lookup}.html", context=data)
    except TemplateDoesNotExist:
        html = render_to_string("popups/default.html", context=data)
    return response.JsonResponse({"html": html})


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
    if lookup in LOOKUPS:
        model = LOOKUPS[lookup]
        queryset = model.objects.values(model.geom_data_field, model.choropleth_data_field)
        values = {val[model.geom_data_field]: val[model.choropleth_data_field] for val in queryset}
    else:
        choropleth_data_field = MapLayer.objects.get(layer_identifier=lookup).choropleth_field
        queryset = MVGridDistrictData.objects.values("id", choropleth_data_field)
        values = {val["id"]: val[choropleth_data_field] for val in queryset}

    fill_color = settings.MAP_ENGINE_CHOROPLETH_STYLES.get_fill_color(lookup, list(values.values()))
    return response.JsonResponse({"values": values, "paintProperties": {"fill-color": fill_color, "fill-opacity": 1}})


LOOKUPS: dict[str, str] = {
    "transport_mit_demand": TransportMitDemand,
    "egon_demand_electricity_household_2035": DemandHousehold,
}
