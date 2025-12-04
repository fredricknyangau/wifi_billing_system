from django.db import models

class NetworkQualityMetric(models.Model):
    router_id = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    latency_ms = models.FloatField()
    jitter_ms = models.FloatField()
    packet_loss_percent = models.FloatField()
    cpu_usage_percent = models.FloatField(default=0.0)
    memory_usage_percent = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.router_id} - {self.timestamp}"

class OutageReport(models.Model):
    STATUS_CHOICES = [
        ('DETECTED', 'Detected'),
        ('CONFIRMED', 'Confirmed'),
        ('RESOLVED', 'Resolved'),
    ]
    
    region = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DETECTED')
    detected_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    root_cause = models.TextField(blank=True, null=True)
    estimated_fix_time = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.region} - {self.status} ({self.detected_at})"
