# django imports
from django.utils.translation import ugettext_lazy as _

# lfc imports
from lfc.utils.registration import register_content_type
from lfc.utils.registration import unregister_content_type
from lfc.utils.registration import register_sub_type
from lfc.utils.registration import register_template
from lfc.utils.registration import unregister_template

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


def uninstall():
    """Uninstalls the compositor application.
    """
    # Unregister content types
    unregister_content_type("Composite")

    # Unregister Templates
    unregister_template("Composite")
