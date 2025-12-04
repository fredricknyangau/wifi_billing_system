from compliance.models import ComplianceLog

class DataPrivacyService:
    def anonymize_customer(self, customer, user_performing_action):
        """
        Soft delete customer and scrub PII.
        """
        original_email = customer.user.email
        
        # Scrub PII
        customer.user.username = f"anonymized_{customer.id}"
        customer.user.email = f"anonymized_{customer.id}@deleted.com"
        customer.user.first_name = "Deleted"
        customer.user.last_name = "User"
        customer.user.is_active = False
        customer.user.save()
        
        customer.address = "REDACTED"
        customer.save()
        
        # Log the action
        ComplianceLog.objects.create(
            user=user_performing_action,
            action='DELETE',
            resource=f"Customer: {customer.id}",
            details=f"Anonymized customer {original_email} upon request."
        )
        
        return True
