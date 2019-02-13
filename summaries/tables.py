import django_tables2 as tables
from django_tables2.utils import A

from entities.models import *
from . models import *


class InventoryEntryTable(tables.Table):
    id = tables.LinkColumn(
        'summaries:inventory_detail',
        args=[A('pk')], verbose_name='ID'
    )
    inv_signatur = tables.LinkColumn(
        'summaries:inventory_detail',
        args=[A('pk')], verbose_name='Titel'
    )
    main_person = tables.ManyToManyColumn()
    adm_person = tables.ManyToManyColumn()
    related_person = tables.ManyToManyColumn()
    other_person = tables.ManyToManyColumn()

    class Meta:
        model = InventoryEntry
        sequence = ('id', 'inv_signatur',)
        attrs = {"class": "table table-responsive table-hover"}


class VfbEntryTable(tables.Table):
    id = tables.LinkColumn(
        'summaries:verfachbucheintrag_detail',
        args=[A('pk')], verbose_name='ID'
    )
    title = tables.LinkColumn(
        'summaries:verfachbucheintrag_detail',
        args=[A('pk')], verbose_name='Titel'
    )
    mentioned_person = tables.ManyToManyColumn()
    mentioned_inst = tables.ManyToManyColumn()
    mentioned_place = tables.ManyToManyColumn()
    creator_person = tables.ManyToManyColumn()
    creator_inst = tables.ManyToManyColumn()
    forename = tables.Column()

    class Meta:
        model = VfbEntry
        sequence = ('id', 'title',)
        attrs = {"class": "table table-responsive table-hover"}


class VerfachBuchTable(tables.Table):
    id = tables.LinkColumn(
        'summaries:verfachbuch_detail',
        args=[A('pk')], verbose_name='ID'
    )
    title = tables.LinkColumn(
        'summaries:verfachbuch_detail',
        args=[A('pk')], verbose_name='Titel'
    )
    mentioned_person = tables.ManyToManyColumn()
    mentioned_inst = tables.ManyToManyColumn()
    mentioned_place = tables.ManyToManyColumn()
    creator_person = tables.ManyToManyColumn()
    creator_inst = tables.ManyToManyColumn()
    forename = tables.Column()

    class Meta:
        model = VerfachBuch
        sequence = ('id', 'title',)
        attrs = {"class": "table table-responsive table-hover"}
