import django_filters
from django_filters.rest_framework import FilterSet
from dal import autocomplete
from django import forms

from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from entities.models import Institution
from . models import *


class VfbEntryListFilter(FilterSet):
    entry_signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=VfbEntry._meta.get_field('entry_signatur').help_text,
        label=VfbEntry._meta.get_field('entry_signatur').verbose_name
    )
    vollregest = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=VfbEntry._meta.get_field('vollregest').help_text,
        label=VfbEntry._meta.get_field('vollregest').verbose_name
    )
    located_in__year = django_filters.DateFromToRangeFilter(
        help_text=VerfachBuch._meta.get_field('year').help_text,
        label=VerfachBuch._meta.get_field('year').verbose_name
    )
    adm_action_type = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            collection__name__icontains="adm_type"
        ),
        help_text=VfbEntry._meta.get_field('adm_action_type').help_text,
        label=VfbEntry._meta.get_field('adm_action_type').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/concept-by-colleciton-ac/adm_type",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 0,
                },
        )
    )


class VerfachBuchListFilter(django_filters.FilterSet):
    signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=VerfachBuch._meta.get_field('signatur').help_text,
        label=VerfachBuch._meta.get_field('signatur').verbose_name
    )
    year = django_filters.DateFromToRangeFilter(
        help_text=VerfachBuch._meta.get_field('year').help_text,
        label=VerfachBuch._meta.get_field('year').verbose_name
    )


class AnmerkungenListFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Anmerkungen._meta.get_field('text').help_text,
        label=Anmerkungen._meta.get_field('text').verbose_name
    )
