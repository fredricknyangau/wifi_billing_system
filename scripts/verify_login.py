import os
import django
import sys
import requests

sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def verify_user_and_login():
    # Check latest user
    try:
        latest_user = User.objects.latest('date_joined')
        print(f"Latest User: {latest_user.username} (ID: {latest_user.id})")
        print(f"Is Customer: {latest_user.is_customer}")
        print(f"Phone: {latest_user.phone_number}")
        
        # Try to login with this user (assuming password is 'password123' if I created it manually, 
        # but if created via signup form, I don't know the password unless I set it).
        # Since I can't know the password set by the user in the browser, 
        # I will create a TEST user here to verify the API works.
        
        test_username = "test_user_api"
        test_password = "test_password_123"
        
        if not User.objects.filter(username=test_username).exists():
            print(f"Creating test user: {test_username}")
            # Use the API logic (create_user)
            user = User.objects.create_user(
                username=test_username,
                password=test_password,
                email="test@example.com",
                phone_number="0712345678",
                is_customer=True
            )
            from customers.models import Customer
            Customer.objects.create(user=user, phone_number="0712345678")
        else:
            print(f"Test user {test_username} already exists. Resetting password.")
            user = User.objects.get(username=test_username)
            user.set_password(test_password)
            user.save()

        # Test Login API
        print("Testing Login API...")
        response = requests.post('http://localhost:8000/api/v1/auth/login/', json={
            'username': test_username,
            'password': test_password
        })
        
        if response.status_code == 200:
            print("✅ Login Successful!")
            tokens = response.json()
            print(f"Access Token: {tokens['access'][:20]}...")
            
            # Test Refresh API
            print("Testing Refresh API...")
            refresh_response = requests.post('http://localhost:8000/api/v1/auth/refresh/', json={
                'refresh': tokens['refresh']
            })
            if refresh_response.status_code == 200:
                print("✅ Refresh Successful!")
            else:
                print(f"❌ Refresh Failed: {refresh_response.status_code} - {refresh_response.text}")
                
        else:
            print(f"❌ Login Failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_user_and_login()
