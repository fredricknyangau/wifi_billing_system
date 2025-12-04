from django.db import transaction
# CHANGED: Absolute import path
from radius.models import Radcheck, Radreply, Radacct

class RadiusService:
    """
    The 'Remote Control' for FreeRADIUS.
    Handles creating users, setting limits, and checking usage.
    """

    @staticmethod
    def create_voucher(username, password, time_limit_minutes=None, speed_limit=None):
        """
        Creates a new user in the RADIUS database.
        """
        try:
            with transaction.atomic():
                # 1. Create the Login Entry (Input)
                Radcheck.objects.create(
                    username=username,
                    attribute='Cleartext-Password',
                    op=':=',
                    value=password
                )

                # 2. Add Time Limit (Output) -> Goes to Radreply
                if time_limit_minutes:
                    # Convert to seconds because RADIUS speaks in seconds
                    seconds = str(time_limit_minutes * 60)
                    Radreply.objects.create(
                        username=username,
                        attribute='Session-Timeout',
                        op=':=',
                        value=seconds
                    )

                # 3. Add Speed Limit (Output) -> Goes to Radreply
                if speed_limit:
                    # 'Mikrotik-Rate-Limit' is the specific code MikroTik routers understand
                    Radreply.objects.create(
                        username=username,
                        attribute='Mikrotik-Rate-Limit',
                        op=':=',
                        value=speed_limit
                    )
            
            return True, "Voucher created successfully"

        except Exception as e:
            return False, str(e)

    @staticmethod
    def is_user_online(username):
        """Checks if a user has an open session in radacct"""
        return Radacct.objects.filter(username=username, acctstoptime__isnull=True).exists()