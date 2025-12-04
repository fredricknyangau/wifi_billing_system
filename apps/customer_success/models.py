from django.db import models
from customers.models import Customer

class Playbook(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    trigger_event = models.CharField(max_length=50) # e.g., "NEW_SIGNUP", "HIGH_USAGE"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PlaybookStep(models.Model):
    ACTION_CHOICES = [
        ('SEND_SMS', 'Send SMS'),
        ('SEND_EMAIL', 'Send Email'),
        ('ASSIGN_TASK', 'Assign Task'),
        ('WAIT', 'Wait'),
    ]
    
    playbook = models.ForeignKey(Playbook, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField()
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_config = models.JSONField(default=dict, help_text="Config for the action (e.g., message template)")
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.playbook.name} - Step {self.order}: {self.action_type}"

class CustomerJourney(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='journeys')
    playbook = models.ForeignKey(Playbook, on_delete=models.CASCADE)
    current_step = models.ForeignKey(PlaybookStep, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer} - {self.playbook} ({self.status})"
