from decimal import Decimal
from django.utils import timezone
from pricing.models import DynamicPricingRule

class PriceOptimizer:
    def calculate_price(self, base_price, customer=None):
        """
        Calculate the final price based on active rules.
        """
        final_price = Decimal(base_price)
        now = timezone.now()
        current_hour = now.hour
        
        # 1. Time-based discounts
        time_rules = DynamicPricingRule.objects.filter(
            rule_type='TIME', 
            is_active=True,
            start_hour__lte=current_hour,
            end_hour__gte=current_hour
        )
        
        for rule in time_rules:
            discount = final_price * (rule.discount_percent / 100)
            final_price -= discount

        # 2. Loyalty discounts
        if customer:
            # Mock loyalty check - assume created_at exists
            # years_active = (now - customer.created_at).days / 365
            years_active = 1 # Mock
            
            loyalty_rules = DynamicPricingRule.objects.filter(
                rule_type='LOYALTY',
                is_active=True,
                min_months_active__lte=years_active * 12
            )
            
            for rule in loyalty_rules:
                discount = final_price * (rule.discount_percent / 100)
                final_price -= discount
                
        return max(Decimal('0.00'), final_price)
