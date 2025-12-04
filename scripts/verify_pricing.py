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
from pricing.models import DynamicPricingRule, FairUsagePolicy
from pricing.services.price_optimizer import PriceOptimizer
from pricing.services.fup_enforcer import FUPEnforcer

def verify():
    print("--- Starting Pricing Verification ---")
    
    # 1. Setup Data
    username = "test_pricing_user"
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password="password123")
    
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=user)

    # Create Pricing Rule
    DynamicPricingRule.objects.create(
        name="Night Owl",
        rule_type='TIME',
        discount_percent=30.00,
        start_hour=0,
        end_hour=23, # Make it active all day for test
        is_active=True
    )
    
    # Create FUP Policy
    FairUsagePolicy.objects.create(
        name="Standard FUP",
        data_limit_gb=100,
        throttle_speed_mbps=5.0,
        is_active=True
    )
    
    # 2. Test Price Optimizer
    print("\n--- Testing Price Optimizer ---")
    optimizer = PriceOptimizer()
    base_price = Decimal('1000.00')
    final_price = optimizer.calculate_price(base_price, customer)
    print(f"Base Price: {base_price}")
    print(f"Final Price (with 30% discount): {final_price}")
    
    if final_price == Decimal('700.00'):
        print("✅ Price calculation correct")
    else:
        print("❌ Price calculation incorrect")

    # 3. Test FUP Enforcer
    print("\n--- Testing FUP Enforcer ---")
    enforcer = FUPEnforcer()
    
    # Case A: Under limit
    should_throttle, speed = enforcer.check_throttle(customer, current_usage_gb=50)
    print(f"Usage 50GB (Limit 100GB): Throttle={should_throttle}")
    if not should_throttle:
        print("✅ Correctly allowed")
    else:
        print("❌ Incorrectly throttled")
        
    # Case B: Over limit
    should_throttle, speed = enforcer.check_throttle(customer, current_usage_gb=150)
    print(f"Usage 150GB (Limit 100GB): Throttle={should_throttle}, Speed={speed}")
    if should_throttle and speed == 5.0:
        print("✅ Correctly throttled")
    else:
        print("❌ Incorrectly allowed or wrong speed")

if __name__ == "__main__":
    verify()
