from itertools import count

from crispy_forms.helper import FormHelper
from django.conf import settings
from django.db.models import Max, Min
from django.forms import (
    BooleanField,
    Form,
    IntegerField,
    MultipleChoiceField,
    MultiValueField,
    TextInput,
)
from django_select2.forms import Select2MultipleWidget

from . import map_config, models, widgets


def get_layer_visual(layer: map_config.LegendLayer):
    """Returns visualization style switch depending on layer type"""
    if layer.layer.type == "raster":
        return ""
    if layer.layer.type in ("fill", "line"):
        color = layer.get_color()
        if isinstance(color, list):
            return f"background-color: {color[2]};border-right: 0.5rem solid {color[-1]};"
        return f"background-color: {color}"
    if layer.layer.type == "symbol":
        image = settings.MAP_ENGINE_LAYER_STYLES[layer.layer.id]["layout"]["icon-image"]
        image_path = next(x.path for x in settings.MAP_ENGINE_IMAGES if x.name == image)
        return f"background-image: url('/static/{image_path}');background-size: cover;"
    raise ValueError(f"Unknown layer type '{layer.layer.type}'")


class StaticLayerForm(Form):
    switch = BooleanField(
        label=False,
        widget=widgets.SwitchWidget(
            switch_class="form-check form-switch",
            switch_input_class="form-check-input",
        ),
    )

    counter = count()

    def __init__(self, layer: map_config.LegendLayer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = layer
        self.visual = get_layer_visual(layer)
        self.fields["switch"].widget.attrs["id"] = layer.layer.id

        if hasattr(layer.layer.model, "filters"):
            self.has_filters = True
            for filter_ in layer.layer.model.filters:
                if filter_.type == models.LayerFilterType.Range:
                    filter_min = layer.layer.model.vector_tiles.aggregate(Min(filter_.name))[f"{filter_.name}__min"]
                    filter_max = layer.layer.model.vector_tiles.aggregate(Max(filter_.name))[f"{filter_.name}__max"]
                    self.fields[filter_.name] = MultiValueField(
                        label=getattr(layer.layer.model, filter_.name).field.verbose_name,
                        fields=[IntegerField(), IntegerField()],
                        widget=TextInput(
                            attrs={
                                "class": "js-range-slider",
                                "data-type": "double",
                                "data-min": filter_min,
                                "data-max": filter_max,
                                "data-from": filter_min,
                                "data-to": filter_max,
                                "data-grid": True,
                            }
                        ),
                    )
                elif filter_.type == models.LayerFilterType.Dropdown:
                    filter_values = (
                        layer.layer.model.vector_tiles.values_list(filter_.name, flat=True)
                        .order_by(filter_.name)
                        .distinct()
                    )
                    self.fields[filter_.name] = MultipleChoiceField(
                        choices=[(value, value) for value in filter_values],
                        widget=Select2MultipleWidget(attrs={"id": f"{filter_.name}_{next(self.counter)}"}),
                    )
                else:
                    raise ValueError(f"Unknown filter type '{filter_.type}'")

        self.helper = FormHelper(self)
        self.helper.template = "forms/layer.html"
