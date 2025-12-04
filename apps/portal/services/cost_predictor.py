from decimal import Decimal
from apps.pricing.services.price_optimizer import PriceOptimizer

class CostPredictor:
    def predict_cost(self, customer):
        """
        Estimate next bill based on current usage and active pricing rules.
        """
        base_price = Decimal('1000.00') # Mock plan price
        optimizer = PriceOptimizer()
        
        # Calculate current effective price
        current_price = optimizer.calculate_price(base_price, customer)
        
        return {
            'current_bill_estimate': current_price,
            'savings': base_price - current_price
        }
