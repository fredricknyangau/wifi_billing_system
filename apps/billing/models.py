from django.db import models
from radius.services.manager import RadiusService  # Import our new tool!

class PricingPlan(models.Model):
    """
    Defines what you sell.
    Example: '1 Hour Fast' = 10 KES, 60 mins, 5Mbps
    """
    name = models.CharField(max_length=50)  # e.g., "1 Hour Bundle"
    price = models.DecimalField(max_digits=8, decimal_places=2)  # e.g., 10.00
    duration_minutes = models.IntegerField()  # e.g., 60
    speed_limit = models.CharField(max_length=20, help_text="e.g. '2M/5M'")
    
    def __str__(self):
        return f"{self.name} ({self.price} KES)"

class Voucher(models.Model):
    """
    Represents a sold login code.
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('USED', 'Used'),
        ('EXPIRED', 'Expired'),
    ]

    code = models.CharField(max_length=10, unique=True)
    plan = models.ForeignKey(PricingPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # 1. If this is a new voucher (no ID yet), create it in RADIUS
        if not self.pk:
            success, msg = RadiusService.create_voucher(
                username=self.code,
                password=self.code,  # Password = Code for simplicity
                time_limit_minutes=self.plan.duration_minutes,
                speed_limit=self.plan.speed_limit
            )
            if not success:
                raise Exception(f"Failed to create RADIUS user: {msg}")
        
        # 2. Save the record in Django
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code


class Transaction(models.Model):
    # We use this to track the specific request
    checkout_request_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Completed')

    def __str__(self):
        return f"{self.receipt_number} - {self.amount}"