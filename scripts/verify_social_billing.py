import os
import django
import sys
from decimal import Decimal

# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from accounts.models import User
from customers.models import Customer
from billing.models import PricingPlan
from social_billing.services.group_manager import GroupManager
from social_billing.services.split_billing import BillSplitter
from social_billing.services.mpesa_collector import MPesaCollector

def verify():
    print("--- Starting Social Billing Verification ---")
    
    # 1. Setup Data
    print("\n--- Setting up Group ---")
    # Create Plan
    plan, _ = PricingPlan.objects.get_or_create(
        name="Family Plan", 
        price=Decimal('3000.00'), 
        duration_minutes=43200, # 30 days
        speed_limit="50M/50M"
    )
    
    # Create Admin
    try:
        admin_user = User.objects.get(username="group_admin")
    except User.DoesNotExist:
        admin_user = User.objects.create_user(username="group_admin", password="password123")
    admin, _ = Customer.objects.get_or_create(user=admin_user)
    
    # Create Manager
    manager = GroupManager()
    group = manager.create_group(name="Apartment 4B", admin=admin, plan=plan)
    print(f"Group Created: {group}")
    
    # Add Members
    for i in range(2):
        username = f"member_{i}"
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            u = User.objects.create_user(username=username, password="password123")
        c, _ = Customer.objects.get_or_create(user=u)
        manager.add_member(group, c)
        print(f"Added member: {username}")
        
    # 2. Test Bill Splitting
    print("\n--- Testing Bill Splitting ---")
    splitter = BillSplitter()
    shares = splitter.calculate_shares(group)
    
    print(f"Total Plan Cost: {plan.price}")
    print(f"Shares: {shares}")
    
    expected_share = plan.price / 3
    if len(shares) == 3 and list(shares.values())[0] == expected_share:
        print("✅ Shares calculated correctly (Equal Split)")
    else:
        print("❌ Share calculation failed")

    # 3. Test Contribution & Collection
    print("\n--- Testing Contribution ---")
    collector = MPesaCollector()
    
    # Admin pays their share
    admin_member = group.members.get(customer=admin)
    collector.collect_contribution(admin_member, expected_share)
    print(f"Admin paid: {expected_share}")
    
    status = collector.check_group_status(group)
    print(f"Group Status: {status}")
    
    if status == "PENDING":
        print("✅ Status is PENDING (Partial payment)")
    else:
        print("❌ Status check failed (Should be PENDING)")
        
    # Others pay
    for member in group.members.exclude(customer=admin):
        collector.collect_contribution(member, expected_share)
        print(f"Member {member.customer.user.username} paid: {expected_share}")
        
    status = collector.check_group_status(group)
    print(f"Group Status: {status}")
    
    if status == "PAID":
        print("✅ Status is PAID (Full payment)")
    else:
        print("❌ Status check failed (Should be PAID)")

if __name__ == "__main__":
    verify()
