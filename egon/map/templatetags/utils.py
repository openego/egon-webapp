from django import template

register = template.Library()


@register.simple_tag
def separate_layers(switches):
    """Checks if layers should be separated"""
    return (
        any(switch.layer.type.value != 3 for switch in switches) and
        any(switch.layer.type.value == 3 for switch in switches)
    )
