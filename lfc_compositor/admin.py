from django.contrib import admin

from lfc_compositor.models import Composite
admin.site.register(Composite)

from lfc_compositor.models import Row
admin.site.register(Row)
