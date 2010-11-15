# lfc imports
import lfc.utils
from lfc.models import BaseContent

# django imports
from django import forms
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.loader import render_to_string

class ReferenceInput(forms.HiddenInput):
    """A Widget for displaying a search field instead in a <select> box.
    """
    def __init__(self, request, composite, attrs=None):
        """
        """
        self.request = request
        self.composite = composite
        super(ReferenceInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        breadcrumbs = []
        if value:
            obj = BaseContent.objects.get(pk=value)
            temp = obj
            while temp is not None:
                breadcrumbs.insert(0, temp)
                temp = temp.parent
        else:
            obj = lfc.utils.get_portal()

        if obj.parent:
            children = obj.parent.get_children(self.request)
        else:
            children = lfc.utils.get_portal().get_children(self.request)

        html = """<div id="reference-input">"""
        html += render_to_string("lfc_compositor/widgets/reference_input.html", RequestContext(self.request, {
            "obj" : obj,
            "children" : children,
            "composite_id" : self.composite.id,
            "value" : value,
            "breadcrumbs" : breadcrumbs[:-1],
        }))

        html += "</div>"

        return html
