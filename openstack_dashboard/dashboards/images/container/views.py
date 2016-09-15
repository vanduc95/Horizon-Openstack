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

from django.utils.translation import ugettext_lazy as _

from openstack_dashboard.dashboards.images.container \
    import tables as tbl_container

from docker import Client
import time
from horizon import tables


class Container:
    def __init__(self, containerId, image, command, created, state, name):
        self.id = containerId
        self.image = image
        self.command = command
        self.created = created
        self.state = state
        self.name = name


class IndexView(tables.DataTableView):
    # A very simple class-based view...
    template_name = 'images/container/index.html'
    table_class = tbl_container.ContainerDockerTable
    page_title = _("Container")

    def get_data(self):
        # Add data to the context here...
        marker = self.request.GET.get(
            tbl_container.ContainerDockerTable._meta.pagination_param, None)
        search_opts = self.get_filters({'marker': marker, 'paginate': True})
        print search_opts
        filters = {}
        if (search_opts.get('name') != None):
            filters['name'] = search_opts.get('name')
        elif (search_opts.get('id') != None):
            filters['id'] = search_opts.get('id')

        cli = Client(base_url='unix://var/run/docker.sock')
        containers = []
        for ct in cli.containers(all=True, filters=filters):

            created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ct['Created']))
            containers.append(
                Container(ct['Id'][:12], ct['Image'], ct['Command'], created, ct['State'], ct['Names'][0][1:]))
        return containers

    def get_filters(self, filters):
        filter_action = self.table._meta._filter_action
        if filter_action:
            filter_field = self.table.get_filter_field()
            if filter_action.is_api_filter(filter_field):
                filter_string = self.table.get_filter_string()
                if filter_field and filter_string:
                    filters[filter_field] = filter_string
        return filters
