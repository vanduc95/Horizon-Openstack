from django.template import defaultfilters as filters
from django.utils.translation import ugettext_lazy as _
from docker import Client

from horizon import tables


class FilterImageAction(tables.FilterAction):
    # def filter(self, table, imagedocker, filter_string):
    #     q = filter_string.low()
    #     return [image for image in imagedocker
    #                 if q in image.repoTags.low()
    #             ]
    name = "myfilter"


class DeleteImageAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return (
            u"Delete Image",
            u"Delete Images",
            count
        )

    @staticmethod
    def action_past(count):
        return _(
            u"Deleted Image",
            u"Deleted Images",
            count
        )

    def delete(self, request, obj_id):
        cli = Client(base_url='unix://var/run/docker.sock')

        img_re = None
        imgs = cli.images()
        for img in imgs:
            print(img['Id'])
            if img['Id'] == obj_id:
                print('ket qua:', img['Id'])
                img_re = img
                break
        print(img_re)
        cli.remove_image(image=img_re, force=True)


class ImageDockerTable(tables.DataTable):
    repo = tables.Column('repo', verbose_name='Repository')
    tag = tables.Column('tag', verbose_name='Tag')
    created = tables.Column('created', verbose_name='Created', )
    size = tables.Column('size', filters=(filters.filesizeformat,),
                         attrs=({"data-type": "size"}), verbose_name='Size')

    class Meta(object):
        name = "image_docker"
        verbose_name = _("Image Docker")
        table_actions = (FilterImageAction, DeleteImageAction,)
        row_actions = (DeleteImageAction,)


class ContainerDockerTable(tables.DataTable):
    # repo = tables.Column('repo', verbose_name='Repository')
    # tag = tables.Column('tag', verbose_name='Tag')
    # created = tables.Column('created', verbose_name='Created', )
    # size = tables.Column('size', filters=(filters.filesizeformat,),
    #                      attrs=({"data-type": "size"}), verbose_name='Size')

    class Meta(object):
        name = "docker"
        verbose_name = _("Docker")
        table_actions = (FilterImageAction, DeleteImageAction,)
        row_actions = (DeleteImageAction,)
