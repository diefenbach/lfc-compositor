from django.test import TestCase

# compositor imports
from lfc_compositor.models import Column
from lfc_compositor.models import Composite
from lfc_compositor.models import Row
from lfc_compositor.models import TextWidget
from lfc_compositor.models import Image
from lfc_compositor.models import TextWithImage
from lfc_compositor import config

class ModelsTestCase(TestCase):
    """Populate this class with unit tests for your application.
    """
    def setUp(self):
        """
        """
        self.comp = Composite.objects.create(title="Composite 1", slug="composite-1")
        self.r1 = Row.objects.create(parent=self.comp, position=1)
        self.col1 = Column.objects.create(parent=self.r1, position=1)
        self.col2 = Column.objects.create(parent=self.r1, position=2)

    def test_searchable_text(self):
        """
        """
        text1 = TextWidget.objects.create(parent=self.col1, position=1, content="Hurz")
        self.assertEqual(self.comp.searchable_text, "Hurz")

        text2 = TextWidget.objects.create(parent=self.col1, position=1, content="Schnurz")
        self.assertEqual(self.comp.searchable_text, "Hurz Schnurz")

        text3 = TextWithImage.objects.create(parent=self.col2, position=1, content="Knurz")
        self.assertEqual(self.comp.searchable_text, "Hurz Schnurz Knurz")
        
    def test_render_1(self):
        """
        """
        html = self.comp.render()
        self.assertEqual(html, "<table><tr><td></td><td></td></tr></table>")
        
    def test_render_2(self):
        """
        """
        text1 = TextWidget.objects.create(parent=self.col1, position=1, content="Hurz1")
        text2 = TextWidget.objects.create(parent=self.col1, position=2, content="Hurz2")
        text2 = TextWidget.objects.create(parent=self.col2, position=1, content="Hurz3")
        
        html = self.comp.render()
        self.assertEqual(html, "<table><tr><td>Hurz1Hurz2</td><td>Hurz3</td></tr></table>")
        
    def test_render_3(self):
        """
        """
        text1 = TextWidget.objects.create(parent=self.col1, position=1, content="Hurz1")
        image1 = Image.objects.create(parent=self.col2, position=1)

        html = self.comp.render()
        self.assertEqual(html, """<table><tr><td>Hurz1</td><td><img alt="image" src="" /></td></tr></table>""")
        
    def test_render_4(self):
        """
        """
        text_with_image = TextWithImage.objects.create(parent=self.col1, position=1, content="Hurz1", image_position=config.LEFT)
        html = self.comp.render()
        self.assertEqual(html, """<table><tr><td>\n<img alt="image" class="left" src="" /><p>Hurz1</p>\n</td><td></td></tr></table>""")
        
    def test_render_5(self):
        """
        """
        text_with_image = TextWithImage.objects.create(parent=self.col1, position=1, content="Hurz1", image_position=config.RIGHT)
        html = self.comp.render()
        self.assertEqual(html, """<table><tr><td>\n<img alt="image" class="right" src="" /><p>Hurz1</p>\n</td><td></td></tr></table>""")