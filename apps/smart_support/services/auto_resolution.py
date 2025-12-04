from network_intelligence.models import NetworkQualityMetric

class AutoResolutionService:
    def attempt_fix(self, ticket):
        """
        Check if the issue is known and trigger diagnostics.
        """
        subject_lower = ticket.subject.lower()
        
        if 'slow' in subject_lower or 'internet' in subject_lower:
            # Check network status for the customer's region (mocked as 'Westlands' for now)
            # In real app, we'd get region from ticket.customer.address
            region = "Westlands" 
            
            # Check recent metrics
            metrics = NetworkQualityMetric.objects.filter(region=region).order_by('-timestamp')[:1]
            if metrics.exists():
                metric = metrics.first()
                if metric.packet_loss_percent > 1 or metric.latency_ms > 100:
                    return {
                        'resolved': False,
                        'action': 'Network congestion detected in your area. Technicians are alerted.',
                        'diagnosis': f"High latency ({metric.latency_ms}ms) detected."
                    }
            
            return {
                'resolved': False,
                'action': 'Running remote diagnostics on your router...',
                'diagnosis': 'No network-wide issues found.'
            }
            
        return None
