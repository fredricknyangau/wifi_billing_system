from django.utils import timezone

def is_surge_period():
    """
    Determine if currently in a surge period (high demand).
    """
    now = timezone.now()
    hour = now.hour
    
    # Simple time-based surge (e.g., 7 PM - 10 PM)
    if 19 <= hour <= 22:
        return True
        
    # In a real system, this would check real-time network load from Prometheus/Redis
    return False

def get_surge_multiplier():
    if is_surge_period():
        return 1.2 # 20% surge
    return 1.0
