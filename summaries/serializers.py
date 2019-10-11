import json
from rest_framework import serializers
from . models import *


class VerfachBuchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VerfachBuch
        fields = "__all__"


class VfbEntrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VfbEntry
        fields = "__all__"


class AnmerkungenSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Anmerkungen
        fields = "__all__"
