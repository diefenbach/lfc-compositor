# django imports
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# lfc imports
import lfc.utils
from lfc.models import BaseContent
from lfc.utils import render_to_json
from lfc.utils import HttpJsonResponse

# compositor imports
from lfc_compositor.models import Column
from lfc_compositor.models import Composite
from lfc_compositor.models import Row
from lfc_compositor.models import Widget

def load_reference(request, id, template="lfc_compositor/widgets/reference_input.html"):
    """Loads a reference after is has been clicked within the reference
    browser.
    """
    try:
        composite_id = int(request.GET.get("composite"))
    except ValueError, TypeError:
        composite_id = None

    breadcrumbs = []
    try:
        obj = BaseContent.objects.get(pk=id)
    except (BaseContent.DoesNotExist, ValueError):
        obj = lfc.utils.get_portal()
    else:
        temp = obj
        while temp is not None:
            breadcrumbs.insert(0, temp)
            temp = temp.parent

    html = render_to_string(template, RequestContext(request, {
        "obj" : obj,
        "breadcrumbs" : breadcrumbs,
        "children" : obj.get_children(request),
        "composite_id" : composite_id,
    }))

    html = (
        ("#reference-input", html),
    )

    return HttpResponse(render_to_json(html))

def change_width(request, id):
    """Changes the width of the column with passed id.
    """
    column = Column.objects.get(pk=id)
    composite = _get_composite(column)
    composite.check_permission(request.user, "edit")

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

    return HttpResponse(composite.render(request, edit=True))

def move_column(request, id):
    """Moves passed column to passed direction.
    """
    column = Column.objects.get(pk=id)
    composite = _get_composite(column)
    composite.check_permission(request.user, "edit")
    
    direction = request.REQUEST.get("direction", "0")

    if direction == "1":
        column.position += 15
    else:
        column.position -= 15
        if column.position < 0:
            column.position = 0
    column.save()
    update_columns(column.parent)

    html = (
        ("#compose", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def move_row(request, id):
    """Moves passed column to passed direction.
    """
    row = Row.objects.get(pk=id)
    composite = _get_composite(row)    
    composite.check_permission(request.user, "edit")

    direction = request.REQUEST.get("direction", "0")

    if direction == "1":
        row.position += 15
    else:
        row.position -= 15
        if row.position < 0:
            row.position = 0
    row.save()

    update_rows(composite)

    html = (
        ("#compose", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def move_widget(request, id):
    """Moves passed column to passed direction.
    """
    widget = Widget.objects.get(pk=id)
    composite = _get_composite(widget)
    composite.check_permission(request.user, "edit")
    
    direction = request.REQUEST.get("direction", "0")

    if direction == "1":
        widget.position += 15
    else:
        widget.position -= 15
        if widget.position < 0:
            widget.position = 0

    widget.save()    
    update_widgets(widget.parent)

    html = (
        ("#compose", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def add_row(request, id):
    """Adds a row to the composite with passed id.
    """
    composite = Composite.objects.get(pk=id)
    composite.check_permission(request.user, "edit")

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
        ("#compose", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def add_column(request, id):
    """Adds a column to the row with passed id.
    """
    row = Row.objects.get(pk=id)
    composite = _get_composite(row)
    composite.check_permission(request.user, "edit")
    
    amount = Column.objects.filter(parent=row).count()

    try:
        position = int(request.REQUEST.get("position"))
    except (ValueError, TypeError):
        position = (amount+1) * 10
    else:
        position += 5

    column = Column.objects.create(parent=row, position=position)
    update_columns(column.parent)
    

    html = (
        ("#compose", composite.render(request, edit=True)),
    )

    return HttpResponse(render_to_json(html))

def add_widget(request, template="lfc_compositor/widgets/add_form.html"):
    """Displays widget form and adds a widget.
    """
    # Get column
    column_id = request.REQUEST.get("column_id")
    column = Column.objects.get(pk=column_id)

    composite = _get_composite(column)    
    # composite.check_permission(request.user, "edit")

    # Get widget type's form
    type = request.REQUEST.get("type")
    ct = ContentType.objects.filter(model=type)[0]
    mc = ct.model_class()

    # Display widget form
    if request.method == "GET":
        form = mc().form(request, composite)
        result = render_to_string(template, RequestContext(request, {
            "form" : form,
            "column_id" : column_id,
            "type" : type,
        }))

        html = (("#overlay .content", result),)
        return HttpJsonResponse(html, open_overlay=True)

    # Save widget if form is valid
    else:
        amount = Widget.objects.filter(parent=column).count()
        form = mc().form(request, composite, data=request.POST, files=request.FILES)

        if form.is_valid():
            widget = form.save(commit=False)
            widget.parent = column

            widget.position = amount*10

            widget.save()
            update_widgets(column)

            html = (
                ("#compose", composite.render(request, edit=True)),
            )

            return HttpJsonResponse(html, close_overlay=True)

        else:
            result = render_to_string(template, RequestContext(request, {
                "form" : form,
                "column_id" : column_id,
                "type" : type,
            }))

            html = (
                ("#overlay .content", result),
            )

            return HttpJsonResponse(html)

def edit_widget(request, id, template="lfc_compositor/widgets/form.html"):
    """Provides an widget edit form and saves it.
    """
    widget = Widget.objects.get(pk=id)
    widget = widget.get_content_object()
    composite = _get_composite(widget)
    composite.check_permission(request.user, "edit")

    if request.method == "GET":
        form = widget.form(request, composite, instance=widget)
        try:
            if form.template:
                template = form.template
        except AttributeError:
            pass
        form = render_to_string(template, RequestContext(request, {
            "form" : form,
            "widget" : widget,
            "template" : template,
        }))

        return HttpJsonResponse(
            content = [["#overlay .content", form]],
            open_overlay = True, 
            mimetype = "text/plain")

    else:
        form = widget.form(request, composite, instance = widget, 
            data = request.POST, files = request.FILES)
        if form.is_valid():
            form.save()
            composite = (
                ["#compose", composite.render(request, edit=True)],
            )
            return HttpJsonResponse(
                content = composite, 
                close_overlay = True,
            )
        else:
            form = render_to_string(template, RequestContext(request, {
                "form" : form,
                "widget" : widget,
                "template" : template,
            }))

            return HttpJsonResponse([[("#overlay .content", form)]])

def delete_column(request, id):
    """Deletes the column with passed id
    """
    try:
        column = Column.objects.get(pk=id)
    except Column.DoesNotExist:
        pass
    else:
        composite = _get_composite(column)
        composite.check_permission(request.user, "edit")
        row = column.parent
        column.delete()

    update_columns(row)

    html = (("#compose", composite.render(request, edit=True)),)

    json = render_to_json(
        html = html,
        message = _(u"Column has been deleted.")
    )

    return HttpResponse(json)

def delete_row(request, id):
    """Deletes row with passed id.
    """
    try:
        row = Row.objects.get(pk=id)
    except Row.DoesNotExist:
        pass
    else:
        composite = _get_composite(row)
        composite.check_permission(request.user, "edit")        
        row.delete()

    update_rows(composite)

    html = (("#compose", composite.render(request, edit=True)),)

    json = render_to_json(
        html = html,
        message = _(u"Row has been deleted.")
    )

    return HttpResponse(json)

def delete_widget(request, id):
    """Deletes the widget with the passed id.
    """
    try:
        widget = Widget.objects.get(pk=id)
    except Widget.DoesNotExist:
        pass
    else:
        composite = _get_composite(widget)
        composite.check_permission(request.user, "edit")
        widget.delete()

    html = (("#compose", composite.render(request, edit=True)),)

    json = render_to_json(
        html = html,
        message = _(u"Widget has been deleted.")
    )

    return HttpResponse(json)

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