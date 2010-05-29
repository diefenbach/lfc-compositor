# django imports
from django import forms
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# lfc imports
from lfc.fields.autocomplete import AutoCompleteTagInput
from lfc.fields.thumbs import ImageWithThumbsField
from lfc.models import BaseContent

# tagging imports
from tagging.forms import TagField

# compositor imports
from lfc_compositor.config import LEFT

class Composite(BaseContent):
    """A composite can be added to the portal. A composite has only rows.
    """
    def get_searchable_text(self):
        """Collects searchable text from the children.
        """
        searchable_text = ""
        for row in self.get_rows():
            searchable_text += " " + row.get_searchable_text()

        return searchable_text.strip()

    def get_rows(self):
        """Returns the rows of the composite.
        """
        return Row.objects.filter(parent=self)

    def render(self, request):
        """
        """
        content = ""
        for row in self.get_rows():
            content += row.render(request)

        return render_to_string("lfc_compositor/widgets/composite.html", RequestContext(request, {
            "composite" : self,
            "content" : content
        }))

    def form(self, **kwargs):
        """Returns the add/edit form of the page.
        """
        return CompositeForm(**kwargs)

class CompositeForm(forms.ModelForm):
    """
    """
    tags = TagField(widget=AutoCompleteTagInput(), required=False)

    class Meta:
        model = Composite
        fields = ("title", "display_title", "slug", "tags")

class Row(models.Model):
    """A row for composite. A row can have multiple columns.

    **Parameters**:

    parent
        The composite the of the row.
    """
    parent = models.ForeignKey(Composite, verbose_name=_(u"Parent"), related_name="rows")
    position = models.IntegerField(default=1000)

    def __unicode__(self):
        return "Row %s" % self.id

    def get_columns(self):
        """Returns the rows of the composite.
        """
        return self.columns.all()

    def get_searchable_text(self):
        searchable_text = ""
        for col in self.get_columns():
            searchable_text += " " + col.get_searchable_text()

        return searchable_text.strip()

    def render(self, request):
        content = ""
        for column in self.get_columns():
            content += column.render(request)

        return render_to_string("lfc_compositor/widgets/row.html", RequestContext(request, {
            "row" : self,
            "content" : content
        }))

class Column(models.Model):
    """A column can have serveral widgets.

    **Parameters**:

    parent
        The composite the of the row.
    """
    parent = models.ForeignKey(Row, verbose_name=_(u"Parent"), related_name="columns")
    position = models.IntegerField(default=1000)

    def get_searchable_text(self):
        """
        """
        searchable_text = ""
        for widget in self.get_widgets():
            searchable_text += " " + widget.get_content_object().get_searchable_text()

        return searchable_text.strip()

    def get_widgets(self):
        """
        """
        return self.widgets.order_by("position")

    def render(self, request):
        """
        """
        content = ""
        for widget in self.get_widgets():
            content += widget.render(request)

        columns = self.parent.columns.count()

        width = 100 / columns

        return render_to_string("lfc_compositor/widgets/column.html", RequestContext(request, {
            "content" : content,
            "column" : self,
            "width" : width,
        }))

class Widget(models.Model):
    """A widget is a piece of content within a Composite. This class is the
    base class for all widgets of composite.

    **Parameters**:

    parent
        The composite the of the row.

    position
        The position within the parent.

    content_type
        The content_type of the specific instance.
    """
    parent = models.ForeignKey(Column, verbose_name=_(u"Column"), related_name="widgets")
    position = models.IntegerField(_(u"Position"), blank=True, null=True)
    content_type = models.CharField(blank=True, max_length=100)

    class Meta:
        ordering = ("position", )

    def save(self, force_insert=False, force_update=False):
        """
        """
        if self.content_type == "":
            self.content_type = self.__class__.__name__.lower()
        super(Widget, self).save()

        # Save composite in order to reindex searchable text.
        composite = self
        while isinstance(composite, Composite) == False:
            composite = composite.parent

        composite.save()

    def get_content_object(self):
        """Returns the specific content object of the instance. This method
        can be called if one has a BaseContent and want the specific content
        type e.g. Page.
        """
        # TODO: Ugly but works. There must be a cleaner way. isinstance doesn't
        # work of course.
        if self.__class__.__name__.lower() == "widget":
            return getattr(self, self.content_type)
        else:
            return self

    def get_searchable_text(self):
        """Returns the searchable text of the widget.
        """
        return ""

    def render(self, request):
        return self.get_content_object().render(request)

class TextWidget(Widget):
    """A simple text widget.

    **Parameters**:

    parent
        The composite the of the row.

    content
        The text field
    """
    content = models.TextField(_(u"Text"), blank=True)

    def get_searchable_text(self):
        return self.content

    def form(self, **kwargs):
        """Returns the add/edit form of the text widget.
        """
        return TextWidgetForm(**kwargs)

    def render(self, request):
        return render_to_string("lfc_compositor/widgets/text.html", RequestContext(request, {
            "widget" : self,
        }))

class TextWidgetForm(forms.ModelForm):
    class Meta:
        model = TextWidget
        fields = ("position", "content", )

class ImageWidget(Widget):
    """An simple image widget.

    **Parameters**:

    image
        The image file of the ImageWidget.
    """
    size = models.PositiveSmallIntegerField(_(u"Size"), choices=((0, "60x60"), (1, "100x100"), (2, "200x200"), (3, "400x400"), (4, "600x600"), (5, "800x800")), default=2)
    image = ImageWithThumbsField(_(u"Image"), upload_to="uploads",
        sizes=((60, 60), (100, 100), (200, 200), (400, 400), (600, 600), (800, 800)))

    def form(self, **kwargs):
        """Returns the add/edit form of the image widget.
        """
        return ImageWidgetForm(**kwargs)

    def render(self, request):
        """Renders the widget as HTML.
        """
        image_url = getattr(self.image, "url_%s" % self.get_size_display())
        return render_to_string("lfc_compositor/widgets/image.html", RequestContext(request, {
            "widget" : self,
            "image_url" : image_url,
        }))

class ImageWidgetForm(forms.ModelForm):
    class Meta:
        model = ImageWidget
        fields = ("position", "size", "image", )

class TextWithImageWidget(Widget):
    """A text with a image widget. The image can be at the left or right site.

    **Parameters**:

    image_position
        The position of the image: left, right.
    """
    content = models.TextField(_(u"Text"), blank=True)
    image = ImageWithThumbsField(_(u"Image"), upload_to="uploads",
        sizes=((60, 60), (100, 100), (200, 200), (400, 400), (600, 600), (800, 800)))
    image_position = models.IntegerField(_(u"Position"), default = LEFT)
    size = models.PositiveSmallIntegerField(_(u"Size"), choices=((0, "60x60"), (1, "100x100"), (2, "200x200"), (3, "400x400"), (4, "600x600"), (5, "800x800")), default=2)
    
    def get_searchable_text(self):
        return self.content

    def form(self, **kwargs):
        """Returns the add/edit form of the image widget.
        """
        return TextWithImageWidgetForm(**kwargs)

    def render(self, request):
        image_url = getattr(self.image, "url_%s" % self.get_size_display())
        return render_to_string("lfc_compositor/widgets/text_with_image.html", RequestContext(request, {
            "widget" : self,
            "image_url" : image_url,
            "IMAGE_LEFT" : self.image_position == LEFT,
        }))

class TextWithImageWidgetForm(forms.ModelForm):
    class Meta:
        model = TextWithImageWidget
        fields = ("position", "image", "size",  "image_position", "content")

class ReferenceWidget(Widget):
    """A widget to display existing content.

    **Parameters**:

    parent
        The composite the of the row.

    reference
        The referenced content object.
    """
    reference = models.ForeignKey(BaseContent, verbose_name=_(u"Reference"), blank=True, null=True)

    def get_searchable_text(self):
        try:
            return self.reference.get_content_object().get_searchable_text()
        except AttributeError:
            return ""

    def form(self, **kwargs):
        """Returns the add/edit form of the text widget.
        """
        return ReferenceWidgetForm(**kwargs)

    def render(self, request):
        # content = self.reference.get_content_object()
        return render_to_string("lfc_compositor/widgets/reference.html", RequestContext(request, {
            "widget" : self,
        }))

class ReferenceWidgetForm(forms.ModelForm):
    class Meta:
        model = ReferenceWidget
        fields = ("position", "reference", )
