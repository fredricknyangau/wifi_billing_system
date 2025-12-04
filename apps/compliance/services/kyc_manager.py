class KYCManager:
    def validate_id(self, id_number):
        """
        Mock validation of National ID.
        """
        # Mock logic: Valid if 8 digits
        if len(id_number) == 8 and id_number.isdigit():
            return True
        return False

    def store_kyc_data(self, customer, data):
        """
        Encrypt and store sensitive KYC info (mock encryption).
        """
        # Mock encryption by reversing string
        encrypted_data = {k: v[::-1] if isinstance(v, str) else v for k, v in data.items()}
        
        # In real app, save to a secure model or external vault
        # For MVP, we just return the encrypted payload to simulate success
        return {
            'status': 'SECURELY_STORED',
            'customer_id': customer.id,
            'encrypted_payload': encrypted_data
        }
