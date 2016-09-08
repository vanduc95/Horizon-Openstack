import time

from django.utils.translation import ugettext_lazy as _
from docker import Client

from horizon import tabs
from openstack_dashboard import api
from openstack_dashboard.dashboards.images.images_docker import tables as tbl_docker


class Images:
    def __init__(self, imageId, size, repo, tag, created):
        self.id = imageId
        self.size = size
        self.created = created
        self.repo = repo
        self.tag = tag


class Container:
    def __init__(self, containerId, image, command, created, status, name):
        self.id = containerId
        self.image = image
        self.command = command
        self.created = created
        self.status = status
        self.name = name


class ImageDockerTab(tabs.TableTab):
    name = _("Image Docker")
    slug = "image_docker"
    table_classes = (tbl_docker.ImageDockerTable,)
    template_name = ("horizon/common/_detail_table.html")
    # template_name = "images/images_docker/detail_image.html"
    preload = False

    def get_image_docker_data(self):
        cli = Client(base_url='unix://var/run/docker.sock')
        images = []
        for image in cli.images():
            repo = image['RepoTags']
            repoTags = repo[0]
            create = time.asctime(time.localtime(image['Created']))
            repo = repoTags.split(':')[0]
            tag = repoTags.split(':')[1]
            img = Images(image['Id'], image['Size'], repo, tag, create)
            images.append(img)
        return images


class ContainerDockerTab(tabs.TableTab):
    name = _("Container Docker")
    slug = "container_docker"
    table_classes = (tbl_docker.ContainerDockerTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    def get_container_docker_data(self):
        cli = Client(base_url='unix://var/run/docker.sock')
        containers = []
        for ct in cli.containers():
            created = time.asctime(time.localtime(ct['Created']))
            containers.append(Container(ct['Id'][:12], ct['Image'], ct['Command'], created, ct['Status'], ct['Names'][0]))
        return containers


class ImageDockerTabs(tabs.TabGroup):
    slug = "docker_tabs"
    tabs = (ContainerDockerTab, ImageDockerTab,)
    sticky = True
