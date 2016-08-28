from django.utils.translation import ugettext_lazy as _

import horizon

class LogPanels(horizon.PanelGroup):
    slug = "logpanels"
    name = _("LogPanels")
    panels = ('overview','config')

class LogManagement(horizon.Dashboard):
    name = _("Log Management")
    slug = "logmanagement"
    panels = (LogPanels,)  # Add your panels here.
    default_panel = 'overview'  # Specify the slug of the dashboard's default panel.
    permissions = ('openstack.roles.admin',)


horizon.register(LogManagement)
