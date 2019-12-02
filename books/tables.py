import django_tables2 as tables
from django_tables2.utils import A

from browsing.browsing_utils import MergeColumn
from . models import *


class ExemplarTable(tables.Table):
    id = tables.LinkColumn()

    class Meta:
        model = Exemplar
        sequence = ('id',)
        attrs = {"class": "table table-responsive table-hover"}


class CreatorTable(tables.Table):
    id = tables.LinkColumn()
    gnd_geographic_area = tables.columns.ManyToManyColumn()

    class Meta:
        model = Creator
        sequence = ('id', 'name', 'gnd_date_of_death', 'gnd_geographic_area',)
        attrs = {"class": "table table-responsive table-hover"}


class WorkTable(tables.Table):
    id = tables.LinkColumn()
    creator = tables.TemplateColumn(
        "{% for x in record.creator.all %}<li><a href='{{ x.get_absolute_url }}'>{{ x }}</a></li> {% endfor %}",
        orderable=False, verbose_name="Erzeuger"
    )

    class Meta:
        model = Work
        sequence = ('id', 'title', 'creator')
        attrs = {"class": "table table-responsive table-hover"}
