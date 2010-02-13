from django.conf.urls.defaults import *

# URL patterns for compositor
urlpatterns = patterns('compositor.views',
    url(r'^add-row/(?P<id>\d*)$', "add_row", name="composite_add_row"),
    url(r'^add-column/(?P<id>\d*)$', "add_column", name="compositor_add_column"),
    url(r'^add-widget/(?P<id>\d*)$', "add_widget", name="compositor_add_widget"),

    url(r'^get-widget-form/(?P<id>\d*)$', "get_widget_form", name="composite_get_widget_form"),
    url(r'^save-widget/(?P<id>\d*)$', "save_widget", name="composite_save_widget"),
)
