import json
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView

from config.settings.base import PASSWORD, PASSWORD_PROTECTION

from .config import CLUSTER_GEOJSON_FILE, MAP_SYMBOLS, SOURCES, STORE_COLD_INIT, STORE_HOT_INIT, ZOOM_LEVELS
from .forms import StaticLayerForm
from . import map_config


class MapGLView(TemplateView):
    template_name = "map.html"
    extra_context = {
        "password_protected": PASSWORD_PROTECTION,
        "password": PASSWORD,
        "tiling_service_token": settings.MAP_ENGINE_TILING_SERVICE_TOKEN,
        "tiling_service_style_id": settings.MAP_ENGINE_TILING_SERVICE_STYLE_ID,
        "map_symbols": MAP_SYMBOLS,
        "map_layers": [layer.get_layer() for layer in map_config.ALL_LAYERS],
        "area_switches": {
            category: [StaticLayerForm(layer) for layer in layers] for category, layers in map_config.LEGEND.items()
        },
        "use_distilled_mvts": settings.MAP_ENGINE_USE_DISTILLED_MVTS,
        "store_hot_init": STORE_HOT_INIT,
        "zoom_levels": ZOOM_LEVELS,
    }

    def get_context_data(self, **kwargs):
        # Add unique session ID
        session_id = str(uuid.uuid4())
        context = super(MapGLView, self).get_context_data(**kwargs)
        context["session_id"] = session_id
        context["map_sources"] = {map_source.name: map_source.get_source(self.request) for map_source in map_config.SOURCES}

        # Add layer styles
        with open(
            settings.APPS_DIR.path("static").path("styles").path("layer_styles.json"),
            "r",
        ) as regions:
            context["layer_styles"] = json.loads(regions.read())

        # Categorize sources
        categorized_sources = {
            category: [SOURCES[layer.layer.id] for layer in layers if layer.layer.id in SOURCES]
            for category, layers in map_config.LEGEND.items()
        }
        context["sources"] = categorized_sources

        STORE_COLD_INIT["popup_layers"] = map_config.POPUPS
        STORE_COLD_INIT["region_layers"] = [layer.id for layer in map_config.REGION_LAYERS if layer.id.startswith("fill")]

        context["store_cold_init"] = json.dumps(STORE_COLD_INIT)

        return context


def get_clusters(request):
    with open(CLUSTER_GEOJSON_FILE, "r") as geojson_file:
        clusters = json.load(geojson_file)
        return JsonResponse(clusters)
