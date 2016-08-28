from horizon import tables
import json 
from .tables import LogsTable
from openstack_dashboard import api
from horizon import exceptions


class Log:
	def __init__(self, log_id, time, pid, level, name, content):
		self.id = log_id
		self.time = time
		self.pid = pid
		self.level = level
		self.name = name
		self.content = content


class IndexView(tables.DataTableView):
    table_class = LogsTable
    template_name = 'logmanagement/overview/index.html'


    def get_data(self):
        obj = '[{"id": 1, "time": "2015-11-14 00:23:46.664", "pid": 4180, "level": "INFO", "name": "neutron.openstack.common.service", "content": "[req-0174f305-5689-4076-803c-aef774ae45e0 ] Child caught SIGTERM"},' \
              ' {"id": 2, "time": "2015-11-14 00:23:45.889", "pid": 4191, "level": "ERROR", "name": "neutron.openstack.common.service", "content": "[req-0174f305-5689-4076-803c-aef774ae45e0 ] Child caught SIGTERM"},' \
              ' {"id": 3, "time": "2015-11-14 00:23:47.264", "pid": 4200, "level": "INFO", "name": "neutron.openstack.common.service", "content": "[req-0174f305-5689-4076-803c-aef774ae45e0 ] Child caught SIGTERM"},' \
              ' {"id": 4, "time": "2015-11-14 00:23:44.664", "pid": 4180, "level": "WARNING", "name": "neutron.openstack.common.service", "content": "[req-0174f305-5689-4076-803c-aef774ae45e0 ] Child caught SIGTERM"},' \
              ' {"id": 5, "time": "2015-11-14 00:23:48.964", "pid": 4191, "level": "INFO", "name": "neutron.openstack.common.service", "content": "[req-0174f305-5689-4076-803c-aef774ae45e0 ] Child caught SIGTERM"}]'
        logs = json.loads(obj)
        context = []
        for log in logs:
            # if (self.request.method == 'GET' and 'start' in self.request.GET and 'end' in self.request.GET):
            #     if (log['time'] >= self.request.GET['start']) & (log['time'] <= self.request.GET['end']):
            #         context.append(Log(log['id'], log['time'], log['pid'], log['level'], log['name'], log['content']))
            # else:
            context.append(Log(log['id'], log['time'], log['pid'], log['level'], log['name'], log['content']))
        return context

        # context = [Log(1, 1, 1, 1, 1, 1), Log(2, 2, 2, 2, 2, 2)]
        # return context

    # def get_context_data(self, request):
        # instance = self.tab_group.kwargs['instance']
        # log_length = utils.get_log_length(request)
        # try:
        #     data = api.nova.server_console_output(request,
        #                                           instance.id,
        #                                           tail_length=log_length)
        # except Exception:
        #     data = _('Unable to get log for instance "%s".') % instance.id
        #     exceptions.handle(request, ignore=True)
        # return {"instance": instance,
        #         "console_log": data,
        #         "log_length": log_length}
        # data = 'vanduc'
        # return {"console_log": data,}