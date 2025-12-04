from django.utils import timezone
from customer_success.models import CustomerJourney, PlaybookStep
from customer_success.services.action_executor import ActionExecutor

class PlaybookEngine:
    def __init__(self):
        self.executor = ActionExecutor()

    def assign_playbook(self, customer, playbook):
        """
        Starts a customer on a journey.
        """
        # Check if already on this playbook
        if CustomerJourney.objects.filter(customer=customer, playbook=playbook, status='IN_PROGRESS').exists():
            return None
            
        first_step = playbook.steps.first()
        
        journey = CustomerJourney.objects.create(
            customer=customer,
            playbook=playbook,
            current_step=first_step,
            status='IN_PROGRESS'
        )
        
        return journey

    def advance_journey(self, journey):
        """
        Moves to the next step and triggers the action.
        """
        if journey.status != 'IN_PROGRESS':
            return False
            
        current_step = journey.current_step
        
        if not current_step:
            journey.status = 'COMPLETED'
            journey.completed_at = timezone.now()
            journey.save()
            return True
            
        # Execute current step action
        success = self.executor.execute_action(current_step, journey.customer)
        
        if success:
            # Move to next step
            next_step = PlaybookStep.objects.filter(
                playbook=journey.playbook,
                order__gt=current_step.order
            ).order_by('order').first()
            
            journey.current_step = next_step
            if not next_step:
                journey.status = 'COMPLETED'
                journey.completed_at = timezone.now()
            
            journey.save()
            return True
            
        return False
