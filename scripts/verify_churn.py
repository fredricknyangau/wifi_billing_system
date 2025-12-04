import os
import django
import sys

# Setup Django environment
sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from accounts.models import User
from customers.models import Customer
from analytics.tasks import predict_daily_churn, update_health_scores
from analytics.models import ChurnPrediction, CustomerHealthScore

def verify():
    print("--- Starting Verification ---")
    
    # 1. Create Dummy User and Customer
    username = "test_churn_user"
    email = "test_churn@example.com"
    try:
        user = User.objects.get(username=username)
        print(f"User {username} already exists.")
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, email=email, password="password123")
        print(f"Created user {username}")

    try:
        customer = Customer.objects.get(user=user)
        print(f"Customer for {username} already exists.")
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=user, balance=-100.00) # Negative balance to trigger risk
        print(f"Created customer for {username} with negative balance")

    # 2. Run Tasks
    print("\n--- Running Prediction Task ---")
    predict_daily_churn()
    
    print("\n--- Running Health Score Task ---")
    update_health_scores()
    
    # 3. Verify Results
    print("\n--- Verifying Results ---")
    predictions = ChurnPrediction.objects.filter(customer=customer).order_by('-created_at')
    if predictions.exists():
        latest = predictions.first()
        print(f"✅ Churn Prediction created: Risk={latest.risk_level}, Prob={latest.churn_probability:.2f}")
        print(f"   Factors: {latest.factors}")
    else:
        print("❌ No Churn Prediction found!")

    health_score = CustomerHealthScore.objects.filter(customer=customer).first()
    if health_score:
        print(f"✅ Health Score created: Score={health_score.score}, Trend={health_score.trend}")
    else:
        print("❌ No Health Score found!")

if __name__ == "__main__":
    verify()
