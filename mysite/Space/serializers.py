from rest_framework import serializers
from Space.models import Satelite
from django.core.exceptions import ValidationError

class SateliteReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satelite
        fields = '__all__'


class SateliteWriteSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True, write_only=True)
    latitude = serializers.FloatField(source='_latitude', required=True, write_only=True)
    longitude = serializers.FloatField(source='_longitude', required=True, write_only=True)
    message = serializers.CharField(source='_message', required=False, write_only=True)
    distance = serializers.FloatField(source='_distance', required=False, write_only=True)
    class Meta:
        model = Satelite
        fields = ('name', 'latitude', 'longitude', 'message', 'distance')

