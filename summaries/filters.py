import django_filters

from dal import autocomplete
from django import forms

from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from entities.models import Institution
from . models import *


class InventoryEntryListFilter(django_filters.FilterSet):
    inv_signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=InventoryEntry._meta.get_field('inv_signatur').help_text,
        label=InventoryEntry._meta.get_field('inv_signatur').verbose_name
    )
    is_located_in__signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=InventoryEntry._meta.get_field('is_located_in').help_text,
        label=InventoryEntry._meta.get_field('is_located_in').verbose_name
    )
    table_row = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=InventoryEntry._meta.get_field('table_row').help_text,
        label=InventoryEntry._meta.get_field('table_row').verbose_name
    )


class VfbEntryListFilter(django_filters.FilterSet):
    entry_signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=VfbEntry._meta.get_field('entry_signatur').help_text,
        label=VfbEntry._meta.get_field('entry_signatur').verbose_name
    )
    located_in__year = django_filters.DateFromToRangeFilter(
        help_text=VerfachBuch._meta.get_field('year').help_text,
        label=VerfachBuch._meta.get_field('year').verbose_name
    )
    adm_action_type = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            collection__name__icontains="adm-action-type"
        ),
        help_text=VfbEntry._meta.get_field('adm_action_type').help_text,
        label=VfbEntry._meta.get_field('adm_action_type').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/concept-by-colleciton-ac/adm-action-type",
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
