from portal.models import TransparencyLog

class TransparencyReportService:
    def get_logs(self, customer):
        """
        Get transparency logs for the customer.
        """
        logs = TransparencyLog.objects.filter(customer=customer).order_by('-created_at')[:5]
        return logs
