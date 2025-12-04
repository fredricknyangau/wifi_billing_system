import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def get_token(username, password):
    response = requests.post(f"{BASE_URL}/auth/login/", json={"username": username, "password": password})
    if response.status_code != 200:
        print(f"Login failed for {username}: {response.text}")
        sys.exit(1)
    return response.json()["access"]

def verify_transactions(token, username, expected_count):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/billing/transactions/", headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch transactions for {username}: {response.text}")
        sys.exit(1)
    
    count = len(response.json())
    print(f"User {username} sees {count} transactions. Expected: {expected_count}")
    if count != expected_count:
        print("FAIL")
        sys.exit(1)
    print("PASS")

def main():
    print("Verifying RBAC...")
    
    # Admin should see all
    admin_token = get_token("admin_test", "admin_test")
    headers = {"Authorization": f"Bearer {admin_token}"}
    admin_resp = requests.get(f"{BASE_URL}/billing/transactions/", headers=headers)
    admin_count = len(admin_resp.json())
    print(f"Admin sees {admin_count} transactions.")
    
    # User should see own (1)
    user_token = get_token("user_test", "user_test")
    headers = {"Authorization": f"Bearer {user_token}"}
    user_resp = requests.get(f"{BASE_URL}/billing/transactions/", headers=headers)
    user_count = len(user_resp.json())
    print(f"User sees {user_count} transactions.")
    
    if user_count != 1:
        print(f"FAIL: User should see exactly 1 transaction, saw {user_count}")
        sys.exit(1)
        
    if user_count >= admin_count:
        print(f"FAIL: User count ({user_count}) should be less than Admin count ({admin_count})")
        sys.exit(1)

    print("PASS")

if __name__ == "__main__":
    main()
