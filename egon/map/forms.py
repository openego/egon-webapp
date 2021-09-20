
from itertools import count

from crispy_forms.helper import FormHelper
from django.forms import BooleanField, Form, IntegerField, TextInput, MultiValueField, MultipleChoiceField
from django.db.models import Min, Max
from django_select2.forms import Select2MultipleWidget
from raster.models import RasterLayer as RasterModel

from .widgets import SwitchWidget
from .models import LayerFilterType


class StaticLayerForm(Form):
    switch = BooleanField(
        label=False, widget=SwitchWidget(switch_class="form-check form-switch", switch_input_class="form-check-input",),
    )

    counter = count()

    def __init__(self, layer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = layer
        layer_id = layer.source if issubclass(layer.model, RasterModel) else f"fill-{layer.source}"
        self.fields["switch"].widget.attrs["id"] = layer_id

        if hasattr(layer.model, "filters"):
            self.has_filters = True
            for filter_ in layer.model.filters:
                if filter_.type == LayerFilterType.Range:
                    filter_min = layer.model.vector_tiles.aggregate(Min(filter_.name))[f"{filter_.name}__min"]
                    filter_max = layer.model.vector_tiles.aggregate(Max(filter_.name))[f"{filter_.name}__max"]
                    self.fields[filter_.name] = MultiValueField(
                        label=getattr(layer.model, filter_.name).field.verbose_name,
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
                elif filter_.type == LayerFilterType.Dropdown:
                    filter_values = (
                        layer.model.vector_tiles.values_list(filter_.name, flat=True)
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
