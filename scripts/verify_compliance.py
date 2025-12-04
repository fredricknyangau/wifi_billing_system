import os
import django
import sys
from datetime import date

# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from accounts.models import User
from customers.models import Customer
from compliance.services.kyc_manager import KYCManager
from compliance.services.data_privacy import DataPrivacyService
from compliance.services.tax_reporter import TaxReporter
from compliance.models import ComplianceLog

def verify():
    print("--- Starting Compliance Verification ---")
    
    # 1. Setup Data
    username = "compliance_test_user"
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password="password123", email="test@example.com")
    customer, _ = Customer.objects.get_or_create(user=user)
    
    admin_user, _ = User.objects.get_or_create(username="admin_user", defaults={'email': 'admin@example.com'})
    
    # 2. Test KYC Manager
    print("\n--- Testing KYC Manager ---")
    kyc_manager = KYCManager()
    
    # Validate ID
    if kyc_manager.validate_id("12345678"):
        print("✅ ID Validation passed for valid ID")
    else:
        print("❌ ID Validation failed for valid ID")
        
    if not kyc_manager.validate_id("invalid"):
        print("✅ ID Validation passed for invalid ID")
    else:
        print("❌ ID Validation failed for invalid ID")
        
    # Store Data
    result = kyc_manager.store_kyc_data(customer, {'id_number': '12345678'})
    if result['status'] == 'SECURELY_STORED':
        print("✅ KYC Data stored securely")
    else:
        print("❌ KYC Data storage failed")

    # 3. Test Tax Reporter
    print("\n--- Testing Tax Reporter ---")
    reporter = TaxReporter()
    report = reporter.generate_tax_report(date(2025, 1, 1), date(2025, 1, 31))
    print(f"Tax Report: {report}")
    if report['vat_amount'] > 0:
        print("✅ Tax Report generated successfully")
    else:
        print("❌ Tax Report generation failed")

    # 4. Test Data Privacy (Anonymization)
    print("\n--- Testing Data Privacy (Anonymization) ---")
    privacy_service = DataPrivacyService()
    
    success = privacy_service.anonymize_customer(customer, admin_user)
    
    customer.refresh_from_db()
    customer.user.refresh_from_db()
    
    print(f"Customer User: {customer.user.username}")
    print(f"Customer Email: {customer.user.email}")
    
    if "anonymized" in customer.user.username and not customer.user.is_active:
        print("✅ Customer anonymized successfully")
    else:
        print("❌ Customer anonymization failed")
        
    # Check Log
    log = ComplianceLog.objects.last()
    print(f"Compliance Log: {log}")
    if log and log.action == 'DELETE':
        print("✅ Compliance Log created")
    else:
        print("❌ Compliance Log missing")

if __name__ == "__main__":
    verify()
