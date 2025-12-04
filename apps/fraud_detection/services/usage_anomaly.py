from fraud_detection.models import FraudAlert

class UsageAnomalyDetector:
    def check_anomaly(self, customer, current_usage_gb):
        """
        Compare current usage vs historical average (Z-score).
        For MVP, we use a simple threshold multiplier.
        """
        # Mock historical average (e.g., 10 GB)
        avg_usage = 10.0
        threshold_multiplier = 5.0
        
        if current_usage_gb > (avg_usage * threshold_multiplier):
            alert = FraudAlert.objects.create(
                customer=customer,
                alert_type="Usage Spike",
                description=f"Usage {current_usage_gb}GB exceeds average {avg_usage}GB by >{threshold_multiplier}x",
                severity='HIGH',
                status='NEW'
            )
            return alert
        return None
