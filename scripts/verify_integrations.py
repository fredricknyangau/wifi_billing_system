import os
import django
import sys

# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from integrations.services.sms_gateway import SMSGateway
from integrations.services.email_service import EmailService
from integrations.services.payment_gateway import MPesaGateway

def verify():
    print("--- Starting Integrations Verification ---")
    
    # 1. Test SMS Gateway
    print("\n--- Testing SMS Gateway ---")
    sms_gateway = SMSGateway()
    if sms_gateway.send_sms("+254700000000", "Your WiFi bundle is active!"):
        print("✅ SMS sent successfully")
    else:
        print("❌ SMS sending failed")

    # 2. Test Email Service
    print("\n--- Testing Email Service ---")
    email_service = EmailService()
    if email_service.send_email("user@example.com", "Invoice #123", "Please find attached..."):
        print("✅ Email sent successfully")
    else:
        print("❌ Email sending failed")

    # 3. Test Payment Gateway (M-Pesa)
    print("\n--- Testing Payment Gateway (M-Pesa) ---")
    mpesa = MPesaGateway()
    response = mpesa.initiate_payment("+254700000000", 1000, "INV-123")
    print(f"Payment Response: {response}")
    
    if response['status'] == 'PENDING' and 'WS_' in response['transaction_id']:
        print("✅ Payment initiated successfully")
    else:
        print("❌ Payment initiation failed")
        
    status = mpesa.check_status(response['transaction_id'])
    print(f"Payment Status: {status}")
    if status['status'] == 'COMPLETED':
        print("✅ Payment status check passed")

if __name__ == "__main__":
    verify()
