from portal.models import NetworkStatus

class NetworkHealthService:
    def get_health_status(self, customer):
        """
        Returns network status for the customer's area.
        """
        # Mock: Assume customer is in "Nairobi"
        region = "Nairobi"
        status, created = NetworkStatus.objects.get_or_create(region=region)
        
        return {
            'region': region,
            'status': status.status,
            'avg_speed': status.avg_speed_mbps,
            'uptime': status.uptime_percent
        }
