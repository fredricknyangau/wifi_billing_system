import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class PaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, phone_number, amount, account_reference):
        pass

    @abstractmethod
    def check_status(self, transaction_id):
        pass

class MPesaGateway(PaymentGateway):
    def initiate_payment(self, phone_number, amount, account_reference):
        """
        Mock M-Pesa STK Push.
        """
        logger.info(f"Initiating M-Pesa payment for {phone_number}: {amount}")
        print(f"--- M-PESA STK PUSH ---\nPhone: {phone_number}\nAmount: {amount}\nRef: {account_reference}\n-----------------------")
        return {
            'status': 'PENDING',
            'transaction_id': f"WS_{phone_number[-4:]}_{int(amount)}",
            'message': 'STK Push initiated successfully'
        }

    def check_status(self, transaction_id):
        """
        Mock status check.
        """
        return {
            'status': 'COMPLETED',
            'transaction_id': transaction_id
        }
