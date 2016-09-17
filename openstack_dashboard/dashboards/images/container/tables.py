from django.template import defaultfilters as filters_django
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from docker import Client
from horizon.utils import filters as filters_horizon

from horizon import tables


class FilterImageAction(tables.FilterAction):
    # def filter(self, table, imagedocker, filter_string):
    #     q = filter_string.low()
    #     return [image for image in imagedocker
    #                 if q in image.repoTags.low()
    #             ]
    name = "myfilter"


class ContainerFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (('name', _("Container Name ="), True),
                      ('id', _("Id ="), True),)
    # Tham so True moi gui duoc du lieu sang view


class CreateContainer(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Container")
    url = "horizon:images:container:create"
    print url
    classes = ("ajax-modal",)
    icon = "plus"
    # policy_rules = (("image", "add_image"),)


class DeleteContainerAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Image",
            u"Delete Images",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted Image",
            u"Deleted Images",
            count
        )

    def delete(self, request, obj_id):
        cli = Client(base_url='unix://var/run/docker.sock')

        for container in cli.containers(all=True):
            if (container['Id'][:12] == obj_id):
                cli.remove_container(image=container['Names'][0][1:])
                break;


class ImageDockerTable(tables.DataTable):
    repo = tables.Column('repo', verbose_name='Repository')
    tag = tables.Column('tag', verbose_name='Tag')
    created = tables.Column('created', verbose_name='Created')
    size = tables.Column('size', filters=(filters_django.filesizeformat,),
                         attrs=({"data-type": "size"}), verbose_name='Size')

    class Meta(object):
        name = "image_docker"
        verbose_name = _("Image Docker")
        table_actions = (FilterImageAction,)


class ContainerDockerTable(tables.DataTable):
    id = tables.Column('id', verbose_name='Container Id')
    image = tables.Column('image', verbose_name='Image')
    command = tables.Column('command', verbose_name='Command')
    created = tables.Column('created', verbose_name='Created', filters=(filters_horizon.parse_isotime,
                                                                        filters_horizon.timesince_sortable),
                            attrs={'data-type': 'timesince'})
    state = tables.Column('state', verbose_name='State')
    name = tables.Column('name', verbose_name='Name')

    class Meta(object):
        name = "container_docker"
        verbose_name = _("Container Docker")
        table_actions = (ContainerFilterAction, DeleteContainerAction, CreateContainer)
