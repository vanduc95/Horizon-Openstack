import time

from django.utils.translation import ugettext_lazy as _
from docker import Client

from horizon import exceptions
from horizon import tabs
from openstack_dashboard import api
from openstack_dashboard.dashboards.images.images_docker import tables
from openstack_dashboard.dashboards.mydashboard.mypanel import tables as ins_tbl


class Docker:
    def __init__(self, size, imageId, repo, tag, virtualSize, created):
        self.id = imageId
        self.size = size
        self.created = created
        self.imageId = imageId
        self.repo = repo
        self.tag = tag
        self.virtualSize = virtualSize


class ImageDockerTab(tabs.TableTab):
    name = _("Image Docker")
    slug = "image_docker"
    table_classes = (tables.ImageDockerTable,)
    template_name = ("horizon/common/_detail_table.html")
    # template_name = "images/images_docker/detail_image.html"
    preload = False

    def get_image_docker_data(self):
        cli = Client(base_url='unix://var/run/docker.sock')
        docker = []
        for image in cli.images():
            repo = image['RepoTags']
            repoTags = repo[0]
            create = time.asctime(time.localtime(image['Created']))
            repo = repoTags.split(':')[0]
            tag = repoTags.split(':')[1]
            img = Docker(image['Size'], image['Id'], repo, tag, image['VirtualSize'], create)
            docker.append(img)
        return docker


class ContainerDockerTab(tabs.TableTab):
    name = _("Container Docker")
    slug = "container_docker"
    table_classes = (ins_tbl.InstancesTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False


    def get_instances_data(self):
        try:
            marker = self.request.GET.get(
                ins_tbl.InstancesTable._meta.pagination_param, None)

            instances, self._has_more = api.nova.server_list(
                self.request,
                search_opts={'marker': marker, 'paginate': True})

            return instances
        except Exception:
            self._has_more = False
            error_message = _('Unable to get instances')
            exceptions.handle(self.request, error_message)

            return []


class ImageDockerTabs(tabs.TabGroup):
    slug = "docker_tabs"
    tabs = (ImageDockerTab, ContainerDockerTab)
    sticky = True
