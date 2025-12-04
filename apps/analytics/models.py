from django.db import models
from customers.models import Customer

class ChurnPrediction(models.Model):
    RISK_LEVEL_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='churn_predictions')
    churn_probability = models.FloatField(help_text="Probability between 0 and 1")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES)
    factors = models.JSONField(default=dict, help_text="Factors contributing to the score")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.risk_level} ({self.churn_probability:.2f})"

class CustomerHealthScore(models.Model):
    TREND_CHOICES = [
        ('UP', 'Up'),
        ('DOWN', 'Down'),
        ('STABLE', 'Stable'),
    ]

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='health_score')
    score = models.IntegerField(help_text="Score between 0 and 100")
    trend = models.CharField(max_length=20, choices=TREND_CHOICES, default='STABLE')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer} - {self.score}"
