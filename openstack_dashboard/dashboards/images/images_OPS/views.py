from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import messages
from horizon import tables

from openstack_dashboard import api
from openstack_dashboard import policy

from openstack_dashboard.dashboards.images.images_OPS \
    import tables as images_tables

from docker import Client


class IndexView(tables.DataTableView):
    table_class = images_tables.ImagesTable
    template_name = 'images/images_OPS/index.html'
    page_title = _("Images")

    # def has_prev_data(self, table):
    #     return getattr(self, "_prev", False)
    #
    # def has_more_data(self, table):
    #     return getattr(self, "_more", False)

    def get_data(self):
        if not policy.check((("image", "get_images"),), self.request):
            msg = _("Insufficient privilege level to retrieve image list.")
            messages.info(self.request, msg)
            return []
        prev_marker = self.request.GET.get(
            images_tables.ImagesTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                images_tables.ImagesTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        try:
            images, self._more, self._prev = api.glance.image_list_detailed(
                self.request,
                marker=marker,
                paginate=True,
                sort_dir='asc',
                sort_key='name',
                reversed_order=reversed_order
            )

            print images
        except Exception:
            images = []
            self._prev = self._more = False
            exceptions.handle(self.request, _("Unable to retrieve images."))
        # obj = []
        # for a in images:
        #     if(a.disk_format == 'qcow2'):
        #         obj.append(a)
        # return obj
        cli = Client(base_url='unix://var/run/docker.sock')
        print cli.images()[0]

        return images



# from django.utils.translation import ugettext_lazy as _
#
# from horizon import exceptions
# from horizon import tables
# import json
#
# from openstack_dashboard.dashboards.images.images_OPS import tables as log_nova_api_tables
#
# class Log:
#    def __init__(self, log_id, ten):
#    # def __init__(self, log_id, time, pid, level):
#       self.id = log_id
#       self.ten = ten
#    #  self.pid = pid
#    #  self.level = level
#
# class IndexView(tables.DataTableView):
#     # A very simple class-based view...
#     table_class = log_nova_api_tables.LogNovaTable
#     template_name = 'images/images_OPS/index.html'
#     page_title = _("Log nova api")
#
#     # def get_context_data(self, **kwargs):
#     #     context = super(IndexView, self).get_context_data(**kwargs)
#     #     return context
#
#     def get_data(self):
#         # obj = '[{"id": 1, "time": "2015-11-14 00:23:46.664", "pid": 4180, "level": "INFO"}, {"id": 2, "time": "2015-11-14 00:23:46.889", "pid": 4191, "level": "ERROR"}, {"id": 3, "time": "2015-11-14 00:23:47.264", "pid": 4200, "level": "INFO"}, {"id": 4, "time": "2015-11-14 00:23:48.664", "pid": 4180, "level": "WARNING"}, {"id": 5, "time": "2015-11-14 00:23:48.964", "pid": 4191, "level": "INFO"}]'
#         # logs = json.loads(obj)
#         # context = []
#         # for log in logs:
#         #     context.append(Log(log['id'], log['time'], log['pid'], log['level']))
#
#         l1 = Log( '1',"INFO")
#         l2 = Log('2',"ERROR")
#         l3 = Log('3',"ERROR")
#         context = [l1,l2,l3]
#         return context
