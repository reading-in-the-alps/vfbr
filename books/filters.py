import django_filters
from dal import autocomplete

from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from entities.models import Place
from . models import *


class ExemplarListFilter(django_filters.FilterSet):

    related_work__title = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text='Zeichenkette die im Buchtitel vorkommen muss.',
        label=Work._meta.get_field('title').verbose_name
        )

    related_work = django_filters.ModelMultipleChoiceFilter(
        queryset=Work.objects.all(),
        help_text=Exemplar._meta.get_field('related_work').help_text,
        label=Exemplar._meta.get_field('related_work').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="/books-ac/work-autocomplete/",
            )
        )
    certainty = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.all(),
        help_text=Exemplar._meta.get_field('certainty').help_text,
        label=Exemplar._meta.get_field('certainty').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/concept-by-colleciton-ac/certainty",
            )
        )

    class Meta:
        model = Exemplar
        fields = "__all__"


class WorkListFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Work._meta.get_field('title').help_text,
        label=Work._meta.get_field('title').verbose_name
        )
    creator__gnd_geographic_area = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.objects.all(),
        help_text="Herkunft der Erzeuger",
        label="Herkunft der Erzeuger"
    )
    creator__gnd_date_of_death = django_filters.DateFromToRangeFilter(
        help_text="Von-Bis Todesdatum der Erzeuger (YYYY-MM-DD)",
        label="Todesdatum der Erzeuger",
    )
    title_certainty = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.all(),
        help_text=Work._meta.get_field('title_certainty').help_text,
        label=Work._meta.get_field('title_certainty').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/concept-by-colleciton-ac/certainty",
            )
        )

    class Meta:
        model = Work
        fields = "__all__"


class CreatorListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Creator._meta.get_field('name').help_text,
        label=Creator._meta.get_field('name').verbose_name
        )
    legacy_id = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Creator._meta.get_field('legacy_id').help_text,
        label=Creator._meta.get_field('legacy_id').verbose_name
        )
    normdata_id = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Creator._meta.get_field('normdata_id').help_text,
        label=Creator._meta.get_field('normdata_id').verbose_name
        )
    creator_certainty = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.all(),
        help_text=Creator._meta.get_field('creator_certainty').help_text,
        label=Creator._meta.get_field('creator_certainty').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/concept-by-colleciton-ac/certainty",
            )
        )
    gnd_data = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Creator._meta.get_field('gnd_data').help_text,
        label=Creator._meta.get_field('gnd_data').verbose_name
    )
    gnd_geographic_area = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.objects.all(),
        help_text=Creator._meta.get_field('gnd_geographic_area').help_text,
        label=Creator._meta.get_field('gnd_geographic_area').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="/entities-ac/place-autocomplete",
            )
        )
    gnd_date_of_death = django_filters.DateFromToRangeFilter(
        help_text=Creator._meta.get_field('gnd_date_of_death').help_text,
        label=Creator._meta.get_field('gnd_date_of_death').verbose_name,
    )

    class Meta:
        model = Creator
        fields = "__all__"
