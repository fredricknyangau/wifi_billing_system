import os
import django
import sys

# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from accounts.models import User
from customers.models import Customer
from customer_success.models import Playbook, PlaybookStep, CustomerJourney
from customer_success.services.playbook_engine import PlaybookEngine

def verify():
    print("--- Starting Customer Success Verification ---")
    
    # 1. Setup Data
    username = "playbook_test_user"
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password="password123", email="playbook@example.com")
    customer, _ = Customer.objects.get_or_create(user=user, defaults={'phone_number': '+254711000000'})
    
    # Create Playbook
    playbook = Playbook.objects.create(name="Onboarding Flow", trigger_event="NEW_SIGNUP")
    
    # Create Steps
    step1 = PlaybookStep.objects.create(
        playbook=playbook,
        order=1,
        action_type='SEND_SMS',
        action_config={'message': 'Welcome to our WiFi service!'}
    )
    
    step2 = PlaybookStep.objects.create(
        playbook=playbook,
        order=2,
        action_type='SEND_EMAIL',
        action_config={'subject': 'Getting Started', 'body': 'Here is how to connect...'}
    )
    
    print(f"Playbook Created: {playbook}")
    
    # 2. Test Playbook Assignment
    print("\n--- Testing Playbook Assignment ---")
    engine = PlaybookEngine()
    journey = engine.assign_playbook(customer, playbook)
    
    if journey and journey.status == 'IN_PROGRESS':
        print(f"✅ Journey started: {journey}")
    else:
        print("❌ Journey start failed")
        return

    # 3. Test Step Execution (Step 1: SMS)
    print("\n--- Testing Step 1 Execution (SMS) ---")
    # Advance to execute Step 1
    success = engine.advance_journey(journey)
    if success:
        print("✅ Step 1 executed successfully")
    else:
        print("❌ Step 1 execution failed")
        
    journey.refresh_from_db()
    print(f"Current Step: {journey.current_step}")
    if journey.current_step == step2:
        print("✅ Moved to Step 2")
    else:
        print(f"❌ Failed to move to Step 2 (Current: {journey.current_step})")

    # 4. Test Step Execution (Step 2: Email)
    print("\n--- Testing Step 2 Execution (Email) ---")
    # Advance to execute Step 2
    success = engine.advance_journey(journey)
    if success:
        print("✅ Step 2 executed successfully")
    else:
        print("❌ Step 2 execution failed")
        
    journey.refresh_from_db()
    if journey.status == 'COMPLETED':
        print("✅ Journey Completed")
    else:
        print(f"❌ Journey not completed (Status: {journey.status})")

if __name__ == "__main__":
    verify()
