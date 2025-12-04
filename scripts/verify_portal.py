import os
import django
import sys
# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from accounts.models import User
from customers.models import Customer
from portal.models import NetworkStatus, TransparencyLog
from portal.services.live_usage_gauge import LiveUsageGauge
from portal.services.cost_predictor import CostPredictor
from portal.services.network_health import NetworkHealthService
from portal.services.transparency_report import TransparencyReportService

def verify():
    print("--- Starting Portal Verification ---")
    
    # 1. Setup Data
    username = "test_portal_user"
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password="password123")
    
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=user)

    # Create Network Status
    NetworkStatus.objects.get_or_create(
        region="Nairobi",
        defaults={'status': 'GOOD', 'avg_speed_mbps': 25.5}
    )
    
    # Create Log
    TransparencyLog.objects.create(
        customer=customer,
        event_type='UPGRADE',
        message="Router firmware upgraded",
        is_public=True
    )
    
    # 2. Test API View
    print("\n--- Testing Dashboard API ---")
    factory = APIRequestFactory()
    view = DashboardDataView.as_view()
    
    request = factory.get('/api/v1/portal/dashboard/')
    force_authenticate(request, user=user)
    
    response = view(request)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.data
        print("✅ API Response OK")
        print(f"   Usage Speed: {data['usage']['speed']} Mbps")
        print(f"   Cost Estimate: {data['cost']['current_bill_estimate']}")
        print(f"   Network Status: {data['network']['status']}")
        print(f"   Logs: {len(data['logs'])} found")
    else:
        print(f"❌ API Failed: {response.data}")

if __name__ == "__main__":
    verify()
