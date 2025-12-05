import requests
import base64
import json
from datetime import datetime
from django.conf import settings

class MpesaClient:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.shortcode = settings.MPESA_SHORTCODE
        self.callback_url = settings.MPESA_CALLBACK_URL
        self.base_url = "https://sandbox.safaricom.co.ke"  # Use sandbox for now

    def get_access_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        headers = {"Authorization": f"Basic {auth}"}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['access_token']

    def stk_push(self, phone_number, amount, account_reference="WiFi Billing", transaction_desc="Internet Purchase"):
        access_token = self.get_access_token()
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()
        
        # --- FIX 1: Auto-Format Phone Number ---
        phone_number = str(phone_number).strip()
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]
        elif phone_number.startswith("+254"):
            phone_number = phone_number[1:]
        
        # Ensure it is now 12 digits (254...)
        if not phone_number.startswith("254") or len(phone_number) != 12:
            raise ValueError(f"Invalid Phone Number format: {phone_number}. Must be 2547XXXXXXXX")

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # --- FIX 2: Ensure Amount is Integer ---
        amount = int(float(amount))

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        print(f"DEBUG: Sending Payload to Safaricom: {json.dumps(payload, indent=2)}")

        response = requests.post(url, json=payload, headers=headers)
        
        # --- FIX 3: Print the REAL Error if it fails ---
        if response.status_code != 200:
            print(f"❌ SAFARICOM ERROR: {response.text}")
            
        response.raise_for_status()
        return response.json()