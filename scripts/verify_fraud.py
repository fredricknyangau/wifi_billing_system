import os
import django
import sys

# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from accounts.models import User
from customers.models import Customer
from fraud_detection.services.usage_anomaly import UsageAnomalyDetector
from fraud_detection.services.simbox_detector import SimBoxDetector

def verify():
    print("--- Starting Fraud Detection Verification ---")
    
    # 1. Setup Data
    username = "fraud_test_user"
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password="password123")
    customer, _ = Customer.objects.get_or_create(user=user)
    
    # 2. Test Usage Anomaly
    print("\n--- Testing Usage Anomaly ---")
    anomaly_detector = UsageAnomalyDetector()
    
    # Normal usage
    alert = anomaly_detector.check_anomaly(customer, 5.0)
    if alert is None:
        print("✅ Normal usage: No alert generated")
    else:
        print("❌ Normal usage: Alert generated incorrectly")
        
    # Spike usage (55GB > 50GB threshold)
    alert = anomaly_detector.check_anomaly(customer, 55.0)
    if alert:
        print(f"✅ Spike usage: Alert generated ({alert.alert_type})")
        print(f"   Description: {alert.description}")
    else:
        print("❌ Spike usage: No alert generated")

    # 3. Test SIM Box Detection
    print("\n--- Testing SIM Box Detection ---")
    simbox_detector = SimBoxDetector()
    
    # Suspicious pattern
    session_data = {
        'uptime_hours': 24,
        'location_variance': 0.05
    }
    
    alert = simbox_detector.analyze_pattern(customer, session_data)
    if alert:
        print(f"✅ SIM Box pattern: Alert generated ({alert.alert_type})")
        print(f"   Severity: {alert.severity}")
    else:
        print("❌ SIM Box pattern: No alert generated")

if __name__ == "__main__":
    verify()
