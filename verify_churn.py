import os
import django
import sys

sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from customers.models import Customer
from apps.analytics.services.churn_predictor import ChurnPredictor
from apps.analytics.services.health_scorer import HealthScorer
from apps.analytics.models import ChurnPrediction, CustomerHealthScore

def verify_churn():
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    print("Creating test user...")
    user, created = User.objects.get_or_create(
        username='churn_test_user',
        defaults={
            'email': 'churn@test.com',
            'first_name': 'Churn',
            'last_name': 'Test',
            'is_active': True
        }
    )
    
    print("Creating test customer...")
    customer, created = Customer.objects.get_or_create(
        user=user,
        defaults={
            'address': '123 Test St',
            'balance': 100.00
        }
    )
    
    print(f"Customer created: {customer}")
    
    print("Predicting churn...")
    predictor = ChurnPredictor()
    prediction = predictor.predict(customer)
    print(f"Churn Prediction: {prediction.churn_probability} ({prediction.risk_level})")
    
    print("Calculating health score...")
    scorer = HealthScorer()
    health_score = scorer.update_score(customer)
    print(f"Health Score: {health_score.score} ({health_score.trend})")
    
    # Verify database records
    db_prediction = ChurnPrediction.objects.get(customer=customer)
    assert db_prediction.id == prediction.id
    print("Churn Prediction saved correctly.")
    
    db_health = CustomerHealthScore.objects.get(customer=customer)
    assert db_health.id == health_score.id
    print("Health Score saved correctly.")
    
    print("Verification Successful!")

if __name__ == '__main__':
    verify_churn()
