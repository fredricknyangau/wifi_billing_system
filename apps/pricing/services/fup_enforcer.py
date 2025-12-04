import logging
from pricing.models import FairUsagePolicy

logger = logging.getLogger(__name__)

class FUPEnforcer:
    def check_throttle(self, customer, current_usage_gb):
        """
        Check if a customer should be throttled.
        """
        # Find applicable policy (mock logic: just take the first active one)
        policy = FairUsagePolicy.objects.filter(is_active=True).first()
        
        if not policy:
            return False, None
            
        if current_usage_gb > policy.data_limit_gb:
            # Check for exceptions (VIP, off-peak, etc. - implemented in algorithms)
            # For MVP, just strict enforcement
            return True, policy.throttle_speed_mbps
            
        return False, None

    def apply_throttle(self, customer, speed_mbps):
        """
        Apply throttling via RADIUS CoA.
        """
        logger.info(f"THROTTLE: Limiting {customer} to {speed_mbps} Mbps")
        # Logic to send CoA packet to RADIUS server
        # radius_client.send_coa(customer.ip, speed_mbps)
        pass
