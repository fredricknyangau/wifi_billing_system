from rest_framework import serializers
from .models import DataUsage

class DataUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataUsage
        fields = '__all__'
