from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters as filters
from horizon import tables



class LogTableFilterAction(tables.FilterAction):
    def filter(self, table, logs, filter_string):
        """Really naive case-insensitive search."""
        # FIXME(gabriel): This should be smarter. Written for demo purposes.
        q = filter_string.lower()

        def comp(log):
            if q in log.name.lower():
                return True
            return False

        return filter(comp, logs)


class LogsTable(tables.DataTable):
    time = tables.Column("time", verbose_name=_("Time"))
    pid = tables.Column("pid", verbose_name=_("PID"))
    level = tables.Column('level', verbose_name=_("Level"))
    name = tables.Column('name', verbose_name=_("Name"))
    content = tables.Column('content', verbose_name=_("Content"))

    class Meta:
        name = "logs"
        verbose_name = _("Logs")
        table_actions = (LogTableFilterAction,)
        multi_select = False