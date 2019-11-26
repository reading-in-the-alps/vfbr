import json
from rest_framework import serializers
from . models import Place, AlternativeName, Person, Institution


class GeoJsonSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        if obj.lng:
            geojson = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(obj.lng), float(obj.lat)]
                    },
                "properties": {
                    "name": obj.name,
                    "placeType": obj.place_type
                }
            }
            return geojson
        else:
            return None


class AlternativeNameSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AlternativeName
        fields = "__all__"


class PlaceHelperSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Place
        fields = "__all__"


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    # alternative_name = AlternativeNameSerializer(many=True)
    part_of = PlaceHelperSerializer(many=False)

    class Meta:
        model = Place
        fields = "__all__"


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    belongs_to_place = PlaceHelperSerializer(many=True)

    class Meta:
        model = Person
        fields = "__all__"


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Institution
        fields = "__all__"
