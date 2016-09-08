# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import datetime
import json
import time

import django.views
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from openstack_dashboard.dashboards.sks.instance import views as instance_views
from openstack_dashboard.dashboards.sks.nova_log_client import nova_log_api
import requests

def get_date_from_input(date_input):
    if date_input is None:
        return None
    elif not date_input:
        return "unspecified"
    else:  # 08/24/2016
        try:
            return datetime.datetime.strptime(date_input, "%m/%d/%Y")
        except ValueError:
            return None


class LineChartView(instance_views.IndexView):
    template_name = 'sks/line_chart_nova_log/line_chart.html'
    page_title = _("Instances Overview")

    def get_context_data(self, **kwargs):
        context = {'cinder_meters': [], 'ipmi_meters': [], 'neutron_meters': []}
        context = super(LineChartView, self).get_context_data(**kwargs)

        return context


class SamplesView(django.views.generic.TemplateView):
    def get(self, request, *args, **kwargs):
        # date_from = request.GET.get('date_from', None)
        # date_to = request.GET.get('date_to', None)
        # log_type = request.GET.get('log_type',None);
        # log_count_per_date_list = nova_log_api.get_nova_logs_count_by_day(
        #     "http://192.168.122.10:9090/nova_log/count_logs_per_date",log_type,
        #     date_from, date_to);
        time.sleep(2)
        # series , data_setting = nova_log_api.get_nova_logs_count_by_day()

        series = [{'meter': u'disk.write.requests', 'data': [{'y': 266376.1843971631, 'x': u'2016-08-27T02:18:30'},
                                                             {'y': 384770.97222222225, 'x': u'2016-08-28T02:18:30'},
                                                             {'y': 504014.0833333333, 'x': u'2016-08-29T02:18:30'},
                                                             {'y': 624130.2013888889, 'x': u'2016-08-30T02:18:31'}],
                   'name': u'admin', 'unit': u'request'}]
        data_setting = {}
        ret = {'series': series, 'settings': data_setting}
        return HttpResponse(json.dumps(ret), content_type='application/json')

        # data_docker = convert()
        # series = [
        #     {'meter': u'disk.write.requests',
        #      'data': data_docker[0],
        #      'name': u'container21', 'unit': u'request'},
        #
        #     {'meter': u'disk.write.requests',
        #      'data': data_docker[1],
        #      'name': u'container2', 'unit': u'request'}
        # ]
        # data_setting = {}
        #
        # ret = {'series': series, 'settings': data_setting}
        # return HttpResponse(json.dumps(ret), content_type='application/json')


def convert():
    url = 'http://localhost:8080/api/v1.2/docker'
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)

    dict = r.json()
    obj1 = []
    obj2 = []


    for stats in dict['/docker/46c2b6bd5498d00d7ead42d9202cdd736b8fe0a5d245b0196f5c753cc5e1174f']['stats']:
        obj1.append({'y':stats['cpu']['usage']['per_cpu_usage'][0], 'x':stats['timestamp'][:19]})

    for stats in dict['/docker/83295baf0211267805476d142a4537140d6950310632bf6270db43d4ec07ac6a']['stats']:
        obj2.append({'y':stats['cpu']['usage']['per_cpu_usage'][0], 'x':stats['timestamp'][:19]})
    print obj1
    print obj2
    return [obj1,obj2]