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

import horizon
from openstack_dashboard.dashboards.images import dashboard


class Images_Ops(horizon.Panel):
    name = _("Images_Ops")
    slug = "images_OPS"
    # panels = ('images_OPS',)  # Add your panels here.
    # default_panel = 'images_OPS'  # Specify the slug of the default panel.


# class Docker(horizon.Panel):
#     name = _("Image Docker")
#     slug = "img_docker"
#     panels = ('img_docker',)
#     default_panel = 'img_docker'

# dashboard.Demo.register(Docker)


dashboard.Images.register(Images_Ops)
