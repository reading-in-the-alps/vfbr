from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from . filters import VfbEntryListFilter


from . serializers import *
from . models import *


class VerfachBuchViewSet(viewsets.ModelViewSet):
    queryset = VerfachBuch.objects.all()
    serializer_class = VerfachBuchSerializer


class VfbEntryViewSet(viewsets.ModelViewSet):
    queryset = VfbEntry.objects.all()
    serializer_class = VfbEntrySerializer
    filterset_class = VfbEntryListFilter


class AnmerkungenViewSet(viewsets.ModelViewSet):
    queryset = Anmerkungen.objects.all()
    serializer_class = AnmerkungenSerializer
