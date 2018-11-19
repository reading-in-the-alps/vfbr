import django_filters

from dal import autocomplete
from django import forms

from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from entities.models import Institution
from . models import VerfachBuch


class VerfachBuchListFilter(django_filters.FilterSet):
    signatur = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=VerfachBuch._meta.get_field('signatur').help_text,
        label=VerfachBuch._meta.get_field('signatur').verbose_name
    )
