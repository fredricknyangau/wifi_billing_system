from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChurnPrediction, CustomerHealthScore
from .serializers import ChurnPredictionSerializer, CustomerHealthScoreSerializer
from .services.churn_predictor import ChurnPredictor
from .services.health_scorer import HealthScorer
from customers.models import Customer

class ChurnPredictionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChurnPrediction.objects.all()
    serializer_class = ChurnPredictionSerializer

    @action(detail=False, methods=['post'], url_path='predict')
    def predict(self, request):
        """
        Manually trigger churn prediction for a customer.
        """
        customer_id = request.data.get('customer_id')
        if not customer_id:
            return Response({'error': 'customer_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            customer = Customer.objects.get(id=customer_id)
            predictor = ChurnPredictor()
            prediction = predictor.predict(customer)
            serializer = self.get_serializer(prediction)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

class CustomerHealthScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomerHealthScore.objects.all()
    serializer_class = CustomerHealthScoreSerializer
