import django_tables2 as tables
from django_tables2.utils import A

from browsing.browsing_utils import MergeColumn
from entities.models import *


class PersonPersonTable(tables.Table):
    id = tables.LinkColumn()
    source = tables.LinkColumn(
        'entities:person_detail',
        args=[A('source.id')], verbose_name='Source'
    )
    rel_type = tables.Column()
    target = tables.LinkColumn(
        'entities:person_detail',
        args=[A('target.id')], verbose_name='Target'
    )

    class Meta:
        model = PersonPerson
        sequence = ('id', 'source', 'rel_type', 'target')
        attrs = {"class": "table table-responsive table-hover"}


class PersonTable(tables.Table):
    id = tables.LinkColumn(
        'entities:person_detail',
        args=[A('pk')], verbose_name='ID'
    )
    name = tables.LinkColumn(
        'entities:person_detail',
        args=[A('pk')], verbose_name='Name'
    )
    mentioned_in_entry = tables.TemplateColumn(
        "{% for x in record.mentioned_in_entry.all %}\
        <a href='{{ x.get_absolute_url }}'>{{ x }} </a>|{% endfor %}",
        orderable=False
    )
    profession = tables.ManyToManyColumn()
    merge = MergeColumn(verbose_name='keep | remove', accessor='pk')

    class Meta:
        model = Person
        sequence = ('id', 'written_name',)
        attrs = {"class": "table table-responsive table-hover"}


class InstitutionTable(tables.Table):
    id = tables.LinkColumn(
        'entities:institution_detail',
        args=[A('pk')], verbose_name='ID'
    )
    written_name = tables.LinkColumn(
        'entities:institution_detail',
        args=[A('pk')], verbose_name='Name'
    )
    location = tables.Column()

    class Meta:
        model = Institution
        sequence = ('id', 'written_name',)
        attrs = {"class": "table table-responsive table-hover"}


class PlaceTable(tables.Table):
    name = tables.LinkColumn(
        'entities:place_detail',
        args=[A('pk')], verbose_name='Name'
    )
    part_of = tables.Column()

    class Meta:
        model = Place
        sequence = ('id', 'name',)
        attrs = {"class": "table table-responsive table-hover"}


class AlternativeNameTable(tables.Table):
    name = tables.LinkColumn(
        'entities:alternativename_detail',
        args=[A('pk')], verbose_name='Name'
    )

    class Meta:
        model = AlternativeName
        sequence = ('name',)
        attrs = {"class": "table table-responsive table-hover"}
