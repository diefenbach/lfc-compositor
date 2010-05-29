from django.conf.urls.defaults import *

# URL patterns for compositor
urlpatterns = patterns('lfc_compositor.views',
    url(r'^add-row/(?P<id>\d*)$', "add_row", name="compositor_add_row"),
    url(r'^delete-row/(?P<id>\d*)$', "delete_row", name="compositor_delete_row"),

    url(r'^add-column/(?P<id>\d*)$', "add_column", name="compositor_add_column"),
    url(r'^delete-column/(?P<id>\d*)$', "delete_column", name="compositor_delete_column"),
    
    
    url(r'^add-widget/(?P<id>\d*)$', "add_widget", name="compositor_add_widget"),

    url(r'^get-widget-form/(?P<id>\d*)$', "get_widget_form", name="compositor_get_widget_form"),
    url(r'^save-widget/(?P<id>\d*)$', "save_widget", name="compositor_save_widget"),
    url(r'^delete-widget/(?P<id>\d*)$', "delete_widget", name="compositor_delete_widget"),

)
