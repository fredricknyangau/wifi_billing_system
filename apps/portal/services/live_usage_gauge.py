import random

class LiveUsageGauge:
    def get_current_speed(self, customer):
        """
        Get real-time speed for the customer.
        """
        # Mock: Random speed between 0 and plan limit (e.g., 10 Mbps)
        return round(random.uniform(0.5, 10.0), 1)

    def get_usage_forecast(self, customer):
        """
        Predict end-of-month usage.
        """
        # Mock: Current usage * (days in month / current day)
        current_usage = 45.0 # Mock GB
        return {
            'current_usage_gb': current_usage,
            'projected_usage_gb': 75.0,
            'plan_limit_gb': 100
        }
