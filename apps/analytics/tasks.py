from celery import shared_task
from customers.models import Customer
from analytics.models import ChurnPrediction
from analytics.services.churn_predictor import ChurnPredictor
from analytics.services.retention_engine import RetentionEngine
from analytics.services.health_scorer import HealthScorer
import logging

logger = logging.getLogger(__name__)

@shared_task
def predict_daily_churn():
    """
    Daily task to predict churn for all active customers.
    """
    logger.info("Starting daily churn prediction...")
    predictor = ChurnPredictor()
    retention_engine = RetentionEngine()
    
    customers = Customer.objects.all() # In production, filter by active status
    
    for customer in customers:
        try:
            prediction_result = predictor.predict(customer)
            
            # Save prediction
            ChurnPrediction.objects.create(
                customer=customer,
                churn_probability=prediction_result['churn_probability'],
                risk_level=prediction_result['risk_level'],
                factors=prediction_result['factors']
            )
            
            # Trigger retention actions
            retention_engine.trigger_actions(customer, prediction_result)
            
        except Exception as e:
            logger.error(f"Error predicting churn for {customer}: {e}")

@shared_task
def update_health_scores():
    """
    Task to update customer health scores.
    """
    logger.info("Updating customer health scores...")
    scorer = HealthScorer()
    
    customers = Customer.objects.all()
    
    for customer in customers:
        try:
            scorer.update_score(customer)
        except Exception as e:
            logger.error(f"Error updating health score for {customer}: {e}")
