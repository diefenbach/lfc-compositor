from django.test import TestCase

# compositor imports
from lfc_compositor.models import Column
from lfc_compositor.models import Composite
from lfc_compositor.models import Row
from lfc_compositor.models import TextWidget
from lfc_compositor.models import ImageWidget
from lfc_compositor.models import TextWithImageWidget
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

        text3 = TextWithImageWidget.objects.create(parent=self.col2, position=1, content="Knurz")
        self.assertEqual(self.comp.searchable_text, "Hurz Schnurz Knurz")