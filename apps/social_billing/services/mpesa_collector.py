import uuid
from social_billing.models import ContributionLog

class MPesaCollector:
    def collect_contribution(self, member, amount):
        """
        Initiate M-Pesa request (mocked).
        """
        # Mock M-Pesa transaction
        transaction_id = f"MOCK_{uuid.uuid4().hex[:10].upper()}"
        
        log = ContributionLog.objects.create(
            member=member,
            amount=amount,
            transaction_id=transaction_id
        )
        return log

    def check_group_status(self, group):
        """
        Check if the total bill is covered.
        """
        total_cost = group.plan.price
        
        # Sum all contributions for this billing cycle (simplified: all time for MVP)
        total_contributed = sum(
            log.amount for member in group.members.all() 
            for log in member.contributions.all()
        )
        
        if total_contributed >= total_cost:
            return "PAID"
        else:
            return "PENDING"
