from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from . serializers import *
from . models import Place, AlternativeName, Person, Institution
from . api_renderers import GeoJsonRenderer
from entities.filters import PersonListFilter
from rest_framework.settings import api_settings


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    depth = 2


class AlternativNameViewSet(viewsets.ModelViewSet):
    queryset = AlternativeName.objects.all()
    serializer_class = AlternativeNameSerializer


class GeoJsonViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Place.objects.all()
        serializer = GeoJsonSerializer(queryset, many=True)
        return Response(serializer.data)

    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES) + (GeoJsonRenderer,)


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filterset_class = PersonListFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        'name', 'forename', 'legacy_id'
    ]


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
