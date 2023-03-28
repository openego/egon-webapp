from itertools import count

from crispy_forms.helper import FormHelper
from django.conf import settings
from django.forms import BooleanField, Form
from django_mapengine import legend

from . import widgets


def get_layer_visual(layer: legend.LegendLayer):
    """Returns visualization style switch depending on layer type"""
    if layer.style["type"] == "raster":
        return ""
    if layer.style["type"] in ("fill", "line"):
        color = layer.get_color()
        if isinstance(color, list):
            return f"background-color: {color[2]};border-right: 0.5rem solid {color[-1]};"
        return f"background-color: {color}"
    if layer.style["type"] == "symbol":
        image = layer.style["layout"]["icon-image"]
        image_path = next(x.path for x in settings.MAP_ENGINE_IMAGES if x.name == image)
        return f"background-image: url('{image_path}');background-size: cover;"
    raise ValueError(f"Unknown layer type '{layer.style['type']}'")


class StaticLayerForm(Form):
    switch = BooleanField(
        label=False,
        widget=widgets.SwitchWidget(
            switch_class="form-check form-switch",
            switch_input_class="form-check-input",
        ),
    )

    counter = count()

    def __init__(self, layer: legend.LegendLayer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = layer
        self.visual = get_layer_visual(layer)
        self.fields["switch"].widget.attrs["id"] = layer.get_layer_id()

        self.helper = FormHelper(self)
        self.helper.template = "forms/layer.html"
