from rest_framework import serializers
from .models import ChurnPrediction, CustomerHealthScore

class ChurnPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChurnPrediction
        fields = ['id', 'customer', 'churn_probability', 'risk_level', 'factors', 'created_at']
        read_only_fields = ['id', 'created_at']

class CustomerHealthScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerHealthScore
        fields = ['id', 'customer', 'score', 'trend', 'last_updated']
        read_only_fields = ['id', 'last_updated']
