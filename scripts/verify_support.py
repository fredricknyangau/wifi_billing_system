import os
import django
import sys

# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from accounts.models import User
from customers.models import Customer
from network_intelligence.models import NetworkQualityMetric
from smart_support.services.ticket_manager import TicketManager

def verify():
    print("--- Starting Smart Support Verification ---")
    
    # 1. Setup Data
    username = "support_test_user"
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password="password123")
    customer, _ = Customer.objects.get_or_create(user=user)
    
    # Create Network Metric for Auto-Resolution
    NetworkQualityMetric.objects.create(
        router_id="router_001",
        region="Westlands",
        latency_ms=150.0, # High latency
        jitter_ms=5.0,
        packet_loss_percent=2.0
    )
    
    manager = TicketManager()
    
    # 2. Test Ticket Creation & Sentiment Analysis
    print("\n--- Testing Ticket Creation (Negative Sentiment) ---")
    ticket = manager.create_ticket(
        customer=customer,
        subject="Internet is terrible and slow!",
        message="I hate this service. Fix it immediately or I am leaving."
    )
    
    print(f"Ticket Created: {ticket}")
    print(f"Priority: {ticket.priority}")
    print(f"Sentiment: {ticket.analysis.sentiment}")
    print(f"Urgency: {ticket.analysis.urgency_score}")
    
    if ticket.analysis.sentiment == 'NEGATIVE' and ticket.priority in ['HIGH', 'CRITICAL']:
        print("✅ Sentiment analysis correctly identified urgency")
    else:
        print("❌ Sentiment analysis failed")

    # 3. Test Auto-Resolution
    print("\n--- Testing Auto-Resolution ---")
    print(f"Suggested Action: {ticket.analysis.suggested_action}")
    
    if "Network congestion detected" in ticket.analysis.suggested_action:
        print("✅ Auto-resolution correctly identified network issue")
    else:
        print("❌ Auto-resolution failed")

if __name__ == "__main__":
    verify()
