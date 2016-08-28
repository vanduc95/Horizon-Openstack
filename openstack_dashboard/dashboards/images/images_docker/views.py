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
from docker import Client
from django.utils.translation import ugettext_lazy as _
from horizon import tables
from openstack_dashboard.dashboards.images.images_docker import tabs as image_tabs
from horizon import tabs
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import requests
from django.http import HttpResponse
import json


class IndexView(tabs.TabView):
    tab_group_class = image_tabs.ImageDockerTabs
    template_name = 'images/images_docker/index.html'

    # template_name = 'horizon/common/_detail.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        # a = {"name":"vanduc","class":"bk"}
        # print json.dumps(a)
        # print context
        a = {
            "series": [
                {
                    "name": "instance-00000005",
                    "data": [
                        {"y": 171, "x": "2013-08-21T11:22:25"},
                        {"y": 171, "x": "2013-08-21T11:22:25"}
                    ]
                }, {
                    "name": "instance-00000005",
                    "data": [
                        {"y": 171, "x": "2013-08-21T11:22:25"},
                        {"y": 171, "x": "2013-08-21T11:22:25"}
                    ]
                }
            ],
            "settings": {}
        }
        context['demo'] = json.dumps(a)
        return context


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def demo(request):
    if request.method == 'GET':
        return JSONResponse({
            "series": [
                {
                    "name": "instance-00000005",
                    "data": [
                        {"y": 171, "x": "2013-08-21T11:22:25"},
                        {"y": 171, "x": "2013-08-21T11:22:25"}
                    ]
                }, {
                    "name": "instance-00000005",
                    "data": [
                        {"y": 171, "x": "2013-08-21T11:22:25"},
                        {"y": 171, "x": "2013-08-21T11:22:25"}
                    ]
                }
            ],
            "settings": {}
        })
