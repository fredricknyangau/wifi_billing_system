from django.db import models
from customers.models import Customer

class FraudAlert(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('INVESTIGATING', 'Investigating'),
        ('CONFIRMED', 'Confirmed'),
        ('FALSE_POSITIVE', 'False Positive'),
        ('RESOLVED', 'Resolved'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='fraud_alerts')
    alert_type = models.CharField(max_length=100) # e.g., "Usage Spike", "SIM Box Suspected"
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.alert_type} - {self.customer} ({self.severity})"

class SimBoxDetection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='simbox_detections')
    imei = models.CharField(max_length=20, blank=True, null=True)
    imsi = models.CharField(max_length=20, blank=True, null=True)
    cell_id = models.CharField(max_length=50, blank=True, null=True)
    confidence_score = models.FloatField(default=0.0) # 0.0 to 1.0
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SIM Box Suspect - {self.customer} ({self.confidence_score})"
