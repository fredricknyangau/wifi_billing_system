from network_intelligence.models import NetworkQualityMetric, OutageReport
from django.utils import timezone
from datetime import timedelta

class PredictiveMaintenance:
    def check_router_health(self, router_id):
        """
        Analyze CPU/Memory trends for a router.
        """
        # Get metrics for last 24 hours
        now = timezone.now()
        start_time = now - timedelta(hours=24)
        metrics = NetworkQualityMetric.objects.filter(
            router_id=router_id, 
            timestamp__gte=start_time
        ).order_by('timestamp')
        
        if not metrics.exists():
            return {'status': 'UNKNOWN', 'trend': 'NO_DATA'}
            
        # Check for consistent high CPU
        high_cpu_count = sum(1 for m in metrics if m.cpu_usage_percent > 85)
        total_count = metrics.count()
        
        if total_count > 0 and (high_cpu_count / total_count) > 0.5:
             return {'status': 'CRITICAL', 'trend': 'HIGH_CPU'}
             
        return {'status': 'HEALTHY', 'trend': 'STABLE'}

    def predict_failure(self, router_id):
        """
        Return probability of failure in next 24h.
        """
        health = self.check_router_health(router_id)
        
        if health['status'] == 'CRITICAL':
            return 0.85
        elif health['status'] == 'UNKNOWN':
            return 0.0
        else:
            return 0.05
