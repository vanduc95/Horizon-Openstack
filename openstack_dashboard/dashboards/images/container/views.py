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

from openstack_dashboard.dashboards.images.container \
    import tables as tbl_container

from docker import Client
import time
from horizon import tables


class Container:
    def __init__(self, containerId, image, command, created, status, name):
        self.id = containerId
        self.image = image
        self.command = command
        self.created = created
        self.status = status
        self.name = name


class IndexView(tables.DataTableView):
    # A very simple class-based view...
    template_name = 'images/container/index.html'
    table_class = tbl_container.ContainerDockerTable
    page_title = _("Container")

    def get_data(self):
        # Add data to the context here...

        cli = Client(base_url='unix://var/run/docker.sock')
        containers = []
        for ct in cli.containers():
            created = time.asctime(time.localtime(ct['Created']))
            containers.append(
                Container(ct['Id'][:12], ct['Image'], ct['Command'], created, ct['Status'], ct['Names'][0]))
        return containers
