import os
import django
import sys
from django.utils import timezone

# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from network_intelligence.models import NetworkQualityMetric, OutageReport
from network_intelligence.services.quality_monitor import QualityMonitor
from network_intelligence.services.predictive_maintenance import PredictiveMaintenance

def verify():
    print("--- Starting Network Intelligence Verification ---")
    
    # 1. Test Quality Monitor
    print("\n--- Testing Quality Monitor ---")
    monitor = QualityMonitor()
    
    # Ingest some metrics
    router_id = "router_001"
    region = "Westlands"
    
    print(f"Ingesting metrics for {router_id}...")
    monitor.ingest_metrics({
        'router_id': router_id,
        'region': region,
        'latency_ms': 15.0,
        'jitter_ms': 2.0,
        'packet_loss_percent': 0.0,
        'cpu_usage_percent': 40.0
    })
    
    # Ingest bad metrics
    monitor.ingest_metrics({
        'router_id': router_id,
        'region': region,
        'latency_ms': 150.0, # High latency
        'jitter_ms': 5.0,
        'packet_loss_percent': 0.5,
        'cpu_usage_percent': 90.0 # High CPU
    })
    
    score = monitor.calculate_score(region)
    print(f"Region Score: {score}")
    if score < 100:
        print("✅ Score calculation reflects quality drop")
    else:
        print("❌ Score calculation failed")

    # 2. Test Predictive Maintenance
    print("\n--- Testing Predictive Maintenance ---")
    maintenance = PredictiveMaintenance()
    
    # We just added a high CPU metric (90%), but only one. 
    # Let's add more high CPU metrics to trigger the alert.
    for _ in range(5):
        monitor.ingest_metrics({
            'router_id': router_id,
            'region': region,
            'latency_ms': 20.0,
            'jitter_ms': 2.0,
            'packet_loss_percent': 0.0,
            'cpu_usage_percent': 95.0
        })
        
    failure_prob = maintenance.predict_failure(router_id)
    print(f"Failure Probability: {failure_prob}")
    
    if failure_prob > 0.5:
        print("✅ High failure probability detected")
    else:
        print("❌ Failure prediction failed")

    # 3. Test Outage Report
    print("\n--- Testing Outage Report ---")
    OutageReport.objects.create(
        region=region,
        status='CONFIRMED',
        root_cause='Fiber cut'
    )
    report = OutageReport.objects.filter(region=region).first()
    if report:
        print(f"✅ Outage Report created: {report}")
    else:
        print("❌ Outage Report creation failed")

if __name__ == "__main__":
    verify()
