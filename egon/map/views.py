import json

from django.apps import apps
from django.conf import settings
from django.http import HttpRequest, response
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django_mapengine import views

from config.settings.base import PASSWORD, PASSWORD_PROTECTION

from .config import STORE_COLD_INIT, STORE_HOT_INIT
from .models import MapLayer


class MapGLView(TemplateView, views.MapEngineMixin):
    template_name = "map.html"
    extra_context = {
        "password_protected": PASSWORD_PROTECTION,
        "password": PASSWORD,
        "store_hot_init": STORE_HOT_INIT,
    }

    def get_context_data(self, **kwargs):
        # Add unique session ID
        context = super().get_context_data(**kwargs)

        # Categorize sources
        context["layers"] = (
            MapLayer.objects.all().values(
                "category",
                "name",
                "identifier",
                "geom_layer",
                "description",
                "sub_category",
                "order_priority",
                "colors",
                "icon",
                "scenario",
                "choropleth_field",
            )
            # needs to be ordered by category and subcategory for "regroup" (in template)
            .order_by("category", "sub_category", "order_priority", "name")
        )
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
    map_layer = MapLayer.objects.get(identifier=lookup)
    data = {
        "title": map_layer.popup_title or map_layer.name,
        "description": map_layer.popup_description or map_layer.description or "",
    }
    data_model = apps.get_model(app_label="map", model_name=map_layer.data_model)
    raw_data = data_model.objects.filter(id=region).values(*map_layer.popup_fields)[0]

    # Get the model's verbose field names
    verbose_field_names = {field.name: field.verbose_name for field in data_model._meta.get_fields()}
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

    map_layer = MapLayer.objects.get(identifier=lookup)
    data_model = apps.get_model(app_label="map", model_name=map_layer.data_model)
    choropleth_data_field = map_layer.choropleth_field
    queryset = data_model.objects.values_list("id", choropleth_data_field)
    values = dict(queryset)

    fill_color = settings.MAP_ENGINE_CHOROPLETH_STYLES.get_fill_color(lookup, list(values.values()))
    return response.JsonResponse({"values": values, "paintProperties": {"fill-color": fill_color, "fill-opacity": 1}})
