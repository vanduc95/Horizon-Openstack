# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from horizon import views
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from openstack_dashboard.dashboards.images.images_docker import tabs as image_tabs
from horizon import tabs
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import requests
from django.http import HttpResponse
import json
from docker import Client


class IndexView(tabs.TabView):
    tab_group_class = image_tabs.ImageDockerTabs
    template_name = 'images/images_docker/index.html'

    # template_name = 'horizon/common/_detail.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # a = {
        #     "series": [
        #         {
        #             "name": "instance5",
        #             "data": [
        #                 {"y": 171, "x": "2013-08-21T11:22:25"},
        #                 {"y": 150, "x": "2013-08-21T11:22:25"}
        #             ]
        #         }, {
        #             "name": "instance5",
        #             "data": [
        #                 {"y": 171, "x": "2013-08-21T11:22:25"},
        #                 {"y": 60, "x": "2013-08-21T11:22:25"}
        #             ]
        #         }
        #     ],
        #     "settings": {}
        # }
        # context['demo'] = json.dumps(a)
        # cli = Client(base_url='unix://var/run/docker.sock')
        # stats_obj = cli.stats(container='demo1',decode='true',stream='true')
        # for a in stats_obj:
        #     print(a)
        # print(stats_obj)
        url = 'http://localhost:8080/api/v1.2/docker'
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        info = r.json()
        context['info_container'] = []
        for id in info.keys():
            context['info_container'].append({'name': info[id]['aliases'][0], 'id': id})
        return context


def calculate_cpu_percent(stat):
    cpu_percent = 0.0
    # calculate the change for cpu usage of the
    # container in between readings.
    cpu_delta = stat['cpu_stats']['cpu_usage']['total_usage'] - stat['precpu_stats']['cpu_usage']['total_usage']
    # calculate the change for system usage of the
    # container in between readings.
    system_delta = stat['cpu_stats']['system_cpu_usage'] - stat['precpu_stats']['system_cpu_usage']

    if (system_delta > 0.0 and cpu_delta > 0.0):
        cpu_percent = (cpu_delta / float(system_delta)) * len(stat['cpu_stats']['cpu_usage']['percpu_usage']) * 100.0
        return float("{0:.1f}".format(cpu_percent))

    return cpu_percent


cpu_usage_xy = []


# def convert(id_container):
#     url = 'http://localhost:8080/api/v1.2/docker'
#     headers = {'content-type': 'application/json'}
#     r = requests.get(url, headers=headers)
#     dict = r.json()
#
#     dict_info = {'/docker/83295baf0211267805476d142a4537140d6950310632bf6270db43d4ec07ac6a': 'demo1',
#                  '/docker/83dd3fce3af7995366bb84b77f18e858b6cf50c651b20a567eaaf82898c9da17': 'demo2',
#                  '/docker/dbe6770e3e6cbe1f5fb9c0382f541648f00b29fd6862ba2e0ed2647a784d480e': 'demo3',
#                  '/docker/46c2b6bd5498d00d7ead42d9202cdd736b8fe0a5d245b0196f5c753cc5e1174f': 'cadvisor'}
#     data_xy = []
#     data_y = []
#
#     cli = Client(base_url='unix://var/run/docker.sock')
#     stats_obj = cli.stats(container=dict_info[id_container], decode=True, stream=True)
#     a = 0
#     for stat in stats_obj:
#         if (a < len(dict[id_container]['stats'])):
#             data_y.append(calculate_cpu_percent(stat))
#             print 'wait',a
#             a = a + 1
#         else:
#             break
#
#     i = 0
#     for stats in dict[id_container]['stats']:
#         data_x = stats['timestamp'][:19]
#         # data_xy.append({'y': stats['cpu']['usage']['per_cpu_usage'][0], 'x': data_x})
#         data_xy.append({'y': data_y[i], 'x': data_x})
#         i = i + 1
#
#     return data_xy


def convert(id_container):
    url = 'http://localhost:8080/api/v1.2/docker'
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    dict = r.json()

    dict_info = {'/docker/83295baf0211267805476d142a4537140d6950310632bf6270db43d4ec07ac6a': 'demo1',
                 '/docker/83dd3fce3af7995366bb84b77f18e858b6cf50c651b20a567eaaf82898c9da17': 'demo2',
                 '/docker/dbe6770e3e6cbe1f5fb9c0382f541648f00b29fd6862ba2e0ed2647a784d480e': 'demo3',
                 '/docker/2aea42da8ffb6f6c4328858ab7f8c44654e14c63cc069d7aa20dac9da38fd36b': 'cadvisor1'}
    data_xy = []
    data_y = []

    cli = Client(base_url='unix://var/run/docker.sock')
    stats_obj = cli.stats(container=dict_info[id_container], decode=True, stream=False)
    data_xy = data_xy + cpu_usage_xy
    data_xy.append({'y': calculate_cpu_percent(stats_obj), 'x': stats_obj['read'][:19]})
    cpu_usage_xy.append({'y': calculate_cpu_percent(stats_obj), 'x': stats_obj['read'][:19]})
    # print {'y': calculate_cpu_percent(stats_obj), 'x': stats_obj['read'][:19]}

    # i = 0
    # for stats in dict[id_container]['stats']:
    #     data_x = stats['timestamp'][:19]
    #     # data_xy.append({'y': stats['cpu']['usage']['per_cpu_usage'][0], 'x': data_x})
    #     data_xy.append({'y': data_y[i], 'x': data_x})
    #     i = i + 1
    print data_xy
    return data_xy


def data(request):
    if request.method == 'GET':
        print request.GET['meter']
        data_xy = convert(request.GET['meter'])
        series = [
            {'meter': u'disk.write.requests',
             'data': data_xy,
             'name': u'container21', 'unit': u'request'},
            # {'meter': u'disk.write.requests',
            #  'data': data_docker[1],
            #  'name': u'demo1', 'unit': u'request'},
            #
            # {'meter': u'disk.write.requests',
            #  'data': data_docker[2],
            #  'name': u'demo2', 'unit': u'request'},
            #
            # {'meter': u'disk.write.requests',
            #  'data': data_docker[3],
            #  'name': u'demo3', 'unit': u'request'}
        ]
        data_setting = {}
        linechart = {'series': series, 'settings': data_setting}


        # ret = {
        # "series": [
        #   {
        #     "name": "instance-00000005",
        #     "data": [
        #       {"y": 171, "x": "2013-08-21T11:22:25"},
        #       {"y": 160, "x": "2013-08-21T11:22:25"}
        #     ]
        #   }, {
        #     "name": "instance-00000006",
        #     "data": [
        #       {"y": 50, "x": "2013-08-21T11:22:25"},
        #       {"y": 80, "x": "2013-08-21T11:22:25"}
        #     ]
        #   }
        # ],
        # "settings": {}
        # }
        return HttpResponse(json.dumps(linechart), content_type='application/json')
