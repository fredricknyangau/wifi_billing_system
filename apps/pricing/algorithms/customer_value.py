from decimal import Decimal

def calculate_clv(customer):
    """
    Calculate Customer Lifetime Value (CLV).
    """
    # Mock calculation
    # CLV = Average Monthly Spend * Months Active
    
    avg_spend = Decimal('1000.00') # Mock
    months_active = 12 # Mock
    
    return avg_spend * months_active

def is_vip(customer):
    """
    Determine if a customer is a VIP based on CLV.
    """
    clv = calculate_clv(customer)
    return clv > Decimal('10000.00')
