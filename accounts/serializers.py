from .models import User, Incident
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = '__all__'
