# django imports
from django.utils.translation import ugettext_lazy as _

# lfc imports
from lfc.utils.registration import register_content_type
from lfc.utils.registration import unregister_content_type
from lfc.utils.registration import register_sub_type
from lfc.utils.registration import register_template
from lfc.utils.registration import unregister_template
from lfc.utils.registration import register_resource
from lfc.utils.registration import unregister_resource
from lfc.utils.registration import CSS, JS

# compositor imports
from lfc_compositor.models import Composite

name = "Compositor"
description = _(u"A LFC product to create composite pages out of new and existing content.")

def install():
    """Installs the compositor application.
    """
    # Register Templates
    register_template(name="Composite", path="lfc_compositor/composite.html")

    # Register content types
    register_content_type(Composite, name="Composite", templates=["Composite"], default_template="Composite", workflow="Portal")

    # Register resources
    register_resource(type=CSS, group="manage", path="lfc_compositor/compositor_manage.css")
    register_resource(type=CSS, group="lfc", path="lfc_compositor/compositor.css")
    register_resource(type=JS, group="manage", path="lfc_compositor/compositor.js")

def uninstall():
    """Uninstalls the compositor application.
    """
    # Unregister content types
    unregister_content_type("Composite")

    # Unregister Templates
    unregister_template("Composite")

    # Unregister resources
    unregister_resource(type=CSS, group="manage", path="lfc_compositor/compositor_manage.css")
    unregister_resource(type=CSS, group="lfc", path="lfc_compositor/compositor.css")
    unregister_resource(type=JS, group="manage", path="lfc_compositor/compositor.js")