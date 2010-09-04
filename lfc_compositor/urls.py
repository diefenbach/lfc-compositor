from django.conf.urls.defaults import *

# URL patterns for compositor
urlpatterns = patterns('lfc_compositor.views',
    url(r'^add-row/(?P<id>\d*)$', "add_row", name="compositor_add_row"),
    url(r'^delete-row/(?P<id>\d*)$', "delete_row", name="compositor_delete_row"),

    url(r'^add-column/(?P<id>\d*)$', "add_column", name="compositor_add_column"),
    url(r'^delete-column/(?P<id>\d*)$', "delete_column", name="compositor_delete_column"),
    
    
    url(r'^add-widget$', "add_widget", name="compositor_add_widget"),
    url(r'^add-widget-form$', "add_widget_form", name="compositor_add_widget_form"),

    url(r'^edit-widget-form/(?P<id>\d*)$', "edit_widget_form", name="compositor_edit_widget_form"),
    url(r'^save-widget/(?P<id>\d*)$', "save_widget", name="compositor_save_widget"),
    url(r'^delete-widget/(?P<id>\d*)$', "delete_widget", name="compositor_delete_widget"),

    url(r'^move-column/(?P<id>\d*)$', "move_column", name="compositor_move_column"),
    url(r'^move-row/(?P<id>\d*)$', "move_row", name="compositor_move_row"),
    url(r'^move-widget/(?P<id>\d*)$', "move_widget", name="compositor_move_widget"),
    url(r'^change-width/(?P<id>\d*)$', "change_width", name="compositor_change_width"),

)
