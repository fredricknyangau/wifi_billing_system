import random
from pricing.models import PriceExperiment

class ABTester:
    def get_variant(self, customer, experiment_name):
        """
        Assign a customer to a variant (A or B) for an experiment.
        """
        try:
            experiment = PriceExperiment.objects.get(name=experiment_name, is_active=True)
        except PriceExperiment.DoesNotExist:
            return None
            
        # Simple consistent hashing or random assignment
        # For MVP, just random based on ID parity
        if customer.id % 2 == 0:
            return {
                'variant': 'A',
                'price': experiment.variant_a_price
            }
        else:
            return {
                'variant': 'B',
                'price': experiment.variant_b_price
            }
