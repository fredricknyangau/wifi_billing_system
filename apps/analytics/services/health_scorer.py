from analytics.models import CustomerHealthScore

class HealthScorer:
    def calculate_score(self, customer):
        """
        Calculate customer health score (0-100).
        """
        score = 100
        
        # Deduct for low balance
        if customer.balance < 0:
            score -= 20
            
        # Deduct for no usage (mock)
        # usage = customer.data_usage.last()
        # if not usage:
        #     score -= 10
            
        return max(0, score)

    def update_score(self, customer):
        score = self.calculate_score(customer)
        
        health_score, created = CustomerHealthScore.objects.get_or_create(
            customer=customer,
            defaults={'score': score, 'trend': 'STABLE'}
        )
        
        if not created:
            # Determine trend
            if score > health_score.score:
                health_score.trend = 'UP'
            elif score < health_score.score:
                health_score.trend = 'DOWN'
            else:
                health_score.trend = 'STABLE'
                
            health_score.score = score
            health_score.save()
            
        return health_score
