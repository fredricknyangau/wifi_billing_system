from django.db import models
from customers.models import Customer
from billing.models import PricingPlan

class GroupPlan(models.Model):
    name = models.CharField(max_length=100)
    admin = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='administered_groups')
    plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(GroupPlan, on_delete=models.CASCADE, related_name='members')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='group_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'customer')

    def __str__(self):
        return f"{self.customer} in {self.group}"

class CostSplitter(models.Model):
    SPLIT_TYPE_CHOICES = [
        ('EQUAL', 'Equal Split'),
        ('USAGE', 'Usage Based'),
        ('CUSTOM', 'Custom Percentage'),
    ]
    
    group = models.OneToOneField(GroupPlan, on_delete=models.CASCADE, related_name='cost_splitter')
    split_type = models.CharField(max_length=20, choices=SPLIT_TYPE_CHOICES, default='EQUAL')
    
    def __str__(self):
        return f"{self.group} - {self.split_type}"

class ContributionLog(models.Model):
    member = models.ForeignKey(GroupMember, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True) # M-Pesa ID
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} - {self.amount}"
