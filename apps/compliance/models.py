from django.db import models
from customers.models import Customer
from accounts.models import User

class ComplianceLog(models.Model):
    ACTION_CHOICES = [
        ('ACCESS', 'Data Access'),
        ('MODIFY', 'Data Modification'),
        ('DELETE', 'Data Deletion'),
        ('EXPORT', 'Data Export'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='compliance_actions')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=100) # e.g., "Customer: 123"
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} on {self.resource} by {self.user}"

class DataRetentionPolicy(models.Model):
    data_type = models.CharField(max_length=100, unique=True) # e.g., "Usage Logs"
    retention_period_days = models.IntegerField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.data_type} ({self.retention_period_days} days)"
