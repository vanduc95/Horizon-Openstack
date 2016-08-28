from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import tabs
from horizon import tables
from horizon import exceptions
from horizon import forms

from horizon.utils import memoized

from openstack_dashboard import api

from openstack_dashboard.dashboards.mydashboard.mypanel \
    import forms as project_forms

from openstack_dashboard.dashboards.mydashboard.mypanel \
    import tabs as mydashboard_tabs
from openstack_dashboard.dashboards.mydashboard.mypanel \
    import tables as mytables


class IndexView(tabs.TabbedTableView):
    tab_group_class = mydashboard_tabs.MypanelTabs
    # A very simple class-based view...
    template_name = 'mydashboard/mypanel/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context

    # table_class = mytables.InstancesTable
    # template_name = 'demo/mydemo/index.html'
    # page_title = _("Instances")

    # def has_more_data(self, table):
    #     return self._has_more
    #
    # def get_data(self):
    #     try:
    #         marker = self.request.GET.get(
    #             mytables.InstancesTable._meta.pagination_param, None)
    #
    #         instances, self._has_more = api.nova.server_list(
    #             self.request,
    #             search_opts={'marker': marker, 'paginate': True})
    #
    #         return instances
    #     except Exception:
    #         self._has_more = False
    #         error_message = _('Unable to get instances')
    #         exceptions.handle(self.request, error_message)
    #
    #         return []


class IndexView1(tabs.TabbedTableView):
    tab_group_class = mydashboard_tabs.MypanelTabs
    # A very simple class-based view...
    template_name = 'mydashboard/mypanel/index1.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context

class CreateSnapshotView(forms.ModalFormView):
    form_class = project_forms.CreateSnapshot
    template_name = 'mydashboard/mypanel/create_snapshot.html'
    success_url = reverse_lazy("horizon:project:images:index")
    modal_id = "create_snapshot_modal"
    modal_header = _("Create Snapshot")
    submit_label = _("Create Snapshot")
    submit_url = "horizon:mydashboard:mypanel:create_snapshot"

    @memoized.memoized_method
    def get_object(self):
        try:
            return api.nova.server_get(self.request,
                                       self.kwargs["instance_id"])
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve instance."))

    def get_initial(self):
        return {"instance_id": self.kwargs["instance_id"]}

    def get_context_data(self, **kwargs):
        context = super(CreateSnapshotView, self).get_context_data(**kwargs)
        instance_id = self.kwargs['instance_id']
        context['instance_id'] = instance_id
        context['instance'] = self.get_object()
        context['submit_url'] = reverse(self.submit_url, args=[instance_id])
        return context