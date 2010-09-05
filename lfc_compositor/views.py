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

from lfc.utils import render_to_json

def change_width(request, id):
    """Changes the width of the column with passed id.
    """
    column = Column.objects.get(pk=id)
    width = request.POST.get("width", "")

    if width:
        try:
            width = int(width)
        except ValueError:
            width = None
    else:
        width = None

    column.width = width
    column.save()

    composite = _get_composite(column)
    return HttpResponse(composite.render(request, edit=True))

def move_column(request, id):
    """Moves passed column to passed direction.
    """
    column = Column.objects.get(pk=id)
    direction = request.REQUEST.get("direction", "0")

    if direction == "1":
        column.position += 15
    else:
        column.position -= 15
        if column.position < 0:
            column.position = 0
    column.save()
    update_columns(column.parent)

    composite = _get_composite(column)

    html = (
        ("#core-data-extra", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def move_row(request, id):
    """Moves passed column to passed direction.
    """
    row = Row.objects.get(pk=id)
    direction = request.REQUEST.get("direction", "0")

    if direction == "1":
        row.position += 15
    else:
        row.position -= 15
        if row.position < 0:
            row.position = 0
    row.save()

    composite = _get_composite(row)
    update_rows(composite)

    html = (
        ("#core-data-extra", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def move_widget(request, id):
    """Moves passed column to passed direction.
    """
    widget = Widget.objects.get(pk=id)
    direction = request.REQUEST.get("direction", "0")

    if direction == "1":
        widget.position += 15
    else:
        widget.position -= 15
        if widget.position < 0:
            widget.position = 0

    widget.save()
    composite = _get_composite(widget)
    update_widgets(widget.parent)

    html = (
        ("#core-data-extra", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def edit_widget(request, id, template="lfc_compositor/widgets/form.html"):
    """Returns the form of the widget with the id.
    """
    widget = Widget.objects.get(pk=id)
    widget = widget.get_content_object()

    if request.method == "GET":
        form = widget.form(instance=widget)

        try:
            template = form.template
        except AttributeError:
            pass

        result = render_to_string(template, RequestContext(request, {
            "form" : form,
            "widget" : widget,
            "template" : template,
        }))

        html = (
            ("#overlay .content", result),
        )

        return HttpResponse(render_to_json(html, open=True))

    else:
        form = widget.form(instance=widget, data = request.POST, files = request.FILES)

        if form.is_valid():
            form.save()

            composite = _get_composite(widget)

            html = (
                ("#core-data-extra", composite.render(request, edit=True)),
            )

            return HttpResponse(render_to_json(html, close=True))
        else:
            result = render_to_string(template, RequestContext(request, {
                "form" : form,
                "widget" : widget,
                "template" : template,
            }))

            html = (
                ("#overlay .content", result),
            )

            return HttpResponse(render_to_json(html))

def add_row(request, id):
    """Adds a row to the composite with passed id.
    """
    composite = Composite.objects.get(pk=id)
    
    amount = Row.objects.filter(parent=composite).count()
    
    try:
        position = int(request.REQUEST.get("position"))
    except (ValueError, TypeError):
        position = (amount+1) * 10
    else:
        position += 5

    row = Row.objects.create(parent=composite, position=position)
    
    update_rows(composite)
    
    Column.objects.create(parent=row, position=10)

    html = (
        ("#core-data-extra", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def add_column(request, id):
    """Adds a column to the row with passed id.
    """
    row = Row.objects.get(pk=id)

    amount = Column.objects.filter(parent=row).count()

    try:
        position = int(request.REQUEST.get("position"))
    except (ValueError, TypeError):
        position = (amount+1) * 10
    else:
        position += 5

    column = Column.objects.create(parent=row, position=position)
    update_columns(column.parent)
    composite = _get_composite(row)

    html = (
        ("#core-data-extra", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def add_widget(request, template="lfc_compositor/widgets/add_form.html"):
    """Displays widget form and adds a widget.
    """
    # Get column
    column_id = request.REQUEST.get("column_id")
    column = Column.objects.get(pk=column_id)

    # Get widget type's form
    type = request.REQUEST.get("type")
    ct = ContentType.objects.filter(model=type)[0]
    mc = ct.model_class()

    # Display widget form
    if request.method == "GET":
        form = mc().form()
        result = render_to_string(template, RequestContext(request, {
            "form" : form,
            "column_id" : column_id,
            "type" : type,
        }))

        html = (("#overlay .content", result),)

        return HttpResponse(render_to_json(html, open=True))

    # Save widget if form is valid
    else:
        amount = Widget.objects.filter(parent=column).count()
        form = mc().form(data=request.POST, files=request.FILES)

        if form.is_valid():
            widget = form.save(commit=False)
            widget.parent = column

            widget.position = amount*10

            widget.save()
            update_widgets(column)

            composite = _get_composite(column)

            html = (
                ("#core-data-extra", composite.render(request, edit=True)),
            )

            return HttpResponse(render_to_json(html, close=True))
        else:
            result = render_to_string(template, RequestContext(request, {
                "form" : form,
                "column_id" : column_id,
                "type" : type,
            }))

            html = (
                ("#overlay .content", result),
            )

            return HttpResponse(render_to_json(html))

def delete_column(request, id):
    """Deletes the column with passed id
    """
    try:
        column = Column.objects.get(pk=id)
    except Column.DoesNotExist:
        pass
    else:
        composite = _get_composite(column)
        row = column.parent
        column.delete()

    update_columns(row)

    html = (
        ("#core-data-extra", composite.render(request, edit=True)),
    )

    return HttpResponse(composite.render(request, edit=True))

def delete_row(request, id):
    """Deletes row with passed id.
    """
    try:
        row = Row.objects.get(pk=id)
    except Row.DoesNotExist:
        pass
    else:
        composite = _get_composite(row)
        row.delete()

    update_rows(composite)
    return HttpResponse(composite.render(request, edit=True))

def delete_widget(request, id):
    """Deletes the widget with the passed id.
    """
    try:
        widget = Widget.objects.get(pk=id)
    except Widget.DoesNotExist:
        pass
    else:
        composite = _get_composite(widget)
        widget.delete()

    return HttpResponse(composite.render(request, edit=True))

def _get_composite(obj):
    composite = obj
    while isinstance(composite, Composite) == False:
        composite = composite.parent

    return composite

def update_widgets(column):
    for i, widget in enumerate(Widget.objects.filter(parent=column)):
        widget.position = (i+1) * 10
        widget.save()

def update_rows(composite):
    for i, row in enumerate(Row.objects.filter(parent=composite)):
        row.position = (i+1) * 10
        row.save()

def update_columns(row):
    for i, column in enumerate(Column.objects.filter(parent=row)):
        column.position = (i+1) * 10
        column.save()