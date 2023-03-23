import json

from django.views.generic import TemplateView
from django_mapengine import views

from config.settings.base import PASSWORD, PASSWORD_PROTECTION

from . import map_config
from .config import SOURCES, STORE_COLD_INIT, STORE_HOT_INIT
from .forms import StaticLayerForm


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
