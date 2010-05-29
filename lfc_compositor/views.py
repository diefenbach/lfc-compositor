# django imports
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string

# compositor imports
from lfc_compositor.models import Column
from lfc_compositor.models import Composite
from lfc_compositor.models import Row
from lfc_compositor.models import Widget

def save_widget(request, id):
    """Save the widget with the passed id. Data is passed via POST request.
    """
    widget = Widget.objects.get(pk=id)
    widget = widget.get_content_object()

    form = widget.form(instance=widget, data = request.POST, files = request.FILES)

    if form.is_valid():
        form.save()

    return HttpResponseRedirect(_get_composite(widget).get_absolute_url())

def get_widget_form(request, id, template="lfc_compositor/widgets/form.html"):
    """Returns the form of the widget with the id.
    """
    widget = Widget.objects.get(pk=id)
    widget = widget.get_content_object()

    html = render_to_string(template, RequestContext(request, {
        "form" : widget.form(instance=widget),
        "widget" : widget,
    }))

    return HttpResponse(html)

def _get_composite(obj):
    composite = obj
    while isinstance(composite, Composite) == False:
        composite = composite.parent

    return composite

def add_row(request, id):
    """
    """
    composite = Composite.objects.get(pk=id)
    row = Row.objects.create(parent=composite)

    return HttpResponseRedirect(composite.get_absolute_url())

def delete_row(request, id):
    """
    """
    try:
        row = Row.objects.get(pk=id)
    except Row.DoesNotExist:
        pass
    else:
        row.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def add_column(request, id):
    """
    """
    row = Row.objects.get(pk=id)
    column = Column.objects.create(parent=row)

    return HttpResponseRedirect(_get_composite(row).get_absolute_url())

def delete_column(request, id):
    """
    """
    try:
        column = Column.objects.get(pk=id)
    except Column.DoesNotExist:
        pass
    else:
        column.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def add_widget(request, id):
    """
    """
    column = Column.objects.get(pk=id)

    type = request.REQUEST.get("type")
    ct = ContentType.objects.filter(model=type)[0]
    mc = ct.model_class()
    form = mc().form

    mc.objects.create(parent=column)

    return HttpResponseRedirect(_get_composite(column).get_absolute_url())

def delete_widget(request, id):
    """
    """
    try:
        widget = Widget.objects.get(pk=id)
    except Widget.DoesNotExist:
        pass
    else:
        widget.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))