# django import
from django import template

register = template.Library()

@register.inclusion_tag('lfc_compositor/widgets/render.html', takes_context=True)
def render(context):
    """
    """
    request = context.get("request")
    composite = context.get("lfc_context")

    return {"html" : composite.render(request) }
