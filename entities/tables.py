import django_tables2 as tables
from django_tables2.utils import A

from browsing.browsing_utils import MergeColumn
from entities.models import *


class PersonTable(tables.Table):
    id = tables.LinkColumn(
        'entities:person_detail',
        args=[A('pk')], verbose_name='ID'
    )
    name = tables.LinkColumn(
        'entities:person_detail',
        args=[A('pk')], verbose_name='Name'
    )
    is_main_person = tables.TemplateColumn(
        "{% for x in record.is_main_person.all %}<a href='{{ x.get_absolute_url }}'>{{ x }} </a>|{% endfor %}",
        orderable=False
    )
    is_adm_person = tables.TemplateColumn(
        "{% for x in record.is_adm_person.all %}<a href='{{ x.get_absolute_url }}'>{{ x }} </a>|{% endfor %}",
        orderable=False
    )
    is_related_person = tables.TemplateColumn(
        "{% for x in record.is_related_person.all %}<a href='{{ x.get_absolute_url }}'>{{ x }} </a>|{% endfor %}",
        orderable=False
    )
    is_other_person = tables.TemplateColumn(
        "{% for x in record.is_other_person.all %}<a href='{{ x.get_absolute_url }}'>{{ x }} </a>|{% endfor %}",
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
