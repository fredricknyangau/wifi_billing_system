from django.db import models
from customers.models import Customer

class NetworkStatus(models.Model):
    STATUS_CHOICES = [
        ('GOOD', 'Good'),
        ('CONGESTED', 'Congested'),
        ('OUTAGE', 'Outage'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    region = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='GOOD')
    avg_speed_mbps = models.FloatField(default=0.0)
    uptime_percent = models.FloatField(default=100.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.region} - {self.status}"

class TransparencyLog(models.Model):
    EVENT_TYPE_CHOICES = [
        ('THROTTLE', 'Throttling Applied'),
        ('UPGRADE', 'Network Upgrade'),
        ('OUTAGE', 'Outage Report'),
        ('ALERT', 'Proactive Alert'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transparency_logs', null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event_type} - {self.created_at}"
