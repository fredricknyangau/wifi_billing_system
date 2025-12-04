import logging

logger = logging.getLogger(__name__)

class SMSGateway:
    def send_sms(self, phone_number, message):
        """
        Mock sending SMS. Logs the message.
        """
        logger.info(f"Sending SMS to {phone_number}: {message}")
        print(f"--- SMS SENT to {phone_number} ---\n{message}\n-----------------------------")
        return True
