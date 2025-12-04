from fraud_detection.models import SimBoxDetection, FraudAlert

class SimBoxDetector:
    def analyze_pattern(self, customer, session_data):
        """
        Check for "machine-like" behavior.
        session_data: dict with 'uptime_hours', 'location_variance', 'call_data_ratio'
        """
        uptime = session_data.get('uptime_hours', 0)
        location_variance = session_data.get('location_variance', 1.0) # 0 = static
        
        # Heuristic: High uptime + Static location = Suspicious
        if uptime > 23 and location_variance < 0.1:
            confidence = 0.9
            
            SimBoxDetection.objects.create(
                customer=customer,
                confidence_score=confidence
            )
            
            alert = FraudAlert.objects.create(
                customer=customer,
                alert_type="SIM Box Suspected",
                description=f"High uptime ({uptime}h) and static location detected.",
                severity='CRITICAL',
                status='INVESTIGATING'
            )
            return alert
            
        return None
