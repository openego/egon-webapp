from itertools import product

from django.db.models import BooleanField, IntegerField

from .. import config


def get_color(source_layer):
    if source_layer not in config.LAYER_STYLES:
        raise KeyError(f"Could not find layer '{source_layer}' in layer styles (static/config/layer_styles.json)")
    for color_key in ("fill-color", "line-color", "circle-color"):
        try:
            return config.LAYER_STYLES[source_layer]["paint"][color_key]
        except KeyError:
            continue
    return None


def get_layer_setups(layer):
    setups = []
    setup_model = layer.model._meta.get_field("setup").related_model
    for setup in setup_model._meta.fields:
        if setup.name == "id":
            continue
        if isinstance(setup, IntegerField):
            setups.append([f"{setup.name}={choice[0]}" for choice in setup.choices])
        elif isinstance(setup, BooleanField):
            setups.append([f"{setup.name}=True", f"{setup.name}=False"])
    return product(*setups)
