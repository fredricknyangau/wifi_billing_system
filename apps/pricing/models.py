from django.db import models
from customers.models import Customer

class DynamicPricingRule(models.Model):
    RULE_TYPE_CHOICES = [
        ('TIME', 'Time Based'),
        ('LOYALTY', 'Loyalty Based'),
        ('USAGE', 'Usage Based'),
    ]
    
    name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_hour = models.IntegerField(blank=True, null=True, help_text="0-23")
    end_hour = models.IntegerField(blank=True, null=True, help_text="0-23")
    min_months_active = models.IntegerField(blank=True, null=True, help_text="For loyalty")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.discount_percent}%)"

class FairUsagePolicy(models.Model):
    name = models.CharField(max_length=100)
    data_limit_gb = models.IntegerField()
    throttle_speed_mbps = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.data_limit_gb}GB -> {self.throttle_speed_mbps}Mbps"

class PriceExperiment(models.Model):
    name = models.CharField(max_length=100)
    variant_a_price = models.DecimalField(max_digits=10, decimal_places=2)
    variant_b_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
