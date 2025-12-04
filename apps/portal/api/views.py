from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from portal.services.live_usage_gauge import LiveUsageGauge
from portal.services.cost_predictor import CostPredictor
from portal.services.network_health import NetworkHealthService
from portal.services.transparency_report import TransparencyReportService
from customers.models import Customer

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=404)

        # Services
        usage_gauge = LiveUsageGauge()
        cost_predictor = CostPredictor()
        network_health = NetworkHealthService()
        transparency_report = TransparencyReportService()

        data = {
            'usage': {
                'speed': usage_gauge.get_current_speed(customer),
                'forecast': usage_gauge.get_usage_forecast(customer)
            },
            'cost': cost_predictor.predict_cost(customer),
            'network': network_health.get_health_status(customer),
            'logs': [
                {'event': log.get_event_type_display(), 'message': log.message, 'date': log.created_at}
                for log in transparency_report.get_logs(customer)
            ]
        }
        
        return Response(data)
