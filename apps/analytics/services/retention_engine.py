import logging

logger = logging.getLogger(__name__)

class RetentionEngine:
    def trigger_actions(self, customer, prediction):
        """
        Trigger automated retention actions based on churn prediction.
        """
        risk_level = prediction['risk_level']
        
        if risk_level == 'CRITICAL':
            self._alert_sales_team(customer)
            self._offer_discount(customer, 20)
        elif risk_level == 'HIGH':
            self._send_we_miss_you_sms(customer)
        elif risk_level == 'MEDIUM':
            # Maybe just log it or monitor closely
            pass
            
    def _alert_sales_team(self, customer):
        logger.info(f"ALERT: High churn risk for {customer}. Notify sales.")
        # Logic to create a task for sales team or send email
        
    def _offer_discount(self, customer, percent):
        logger.info(f"OFFER: Sending {percent}% discount to {customer}.")
        # Logic to create a discount code and send SMS
        
    def _send_we_miss_you_sms(self, customer):
        logger.info(f"SMS: Sending 'We miss you' message to {customer}.")
        # Logic to send SMS
