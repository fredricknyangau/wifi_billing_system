from django.core.management.base import BaseCommand
from apps.radius.models import Nas
import sys

class Command(BaseCommand):
    help = 'Interactively add a Mikrotik Router to the NAS table'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Add New Mikrotik Router ---'))

        try:
            # 1. Get Router Name (Identity)
            nasname = input("Enter Router IP Address (e.g., 192.168.88.1): ").strip()
            if not nasname:
                self.stderr.write("IP Address is required.")
                return

            # Check if exists
            if Nas.objects.filter(nasname=nasname).exists():
                self.stderr.write(f"Router with IP {nasname} already exists.")
                return

            # 2. Get Secret
            secret = input("Enter RADIUS Secret (e.g., mysecret123): ").strip()
            if not secret:
                self.stderr.write("Secret is required.")
                return

            # 3. Get Shortname (Optional)
            shortname = input("Enter Short Name (e.g., mikrotik-1) [Optional]: ").strip() or None

            # 4. Get Description (Optional)
            description = input("Enter Description [Optional]: ").strip() or "Mikrotik Router"

            # 5. Create NAS Entry
            nas = Nas.objects.create(
                nasname=nasname,
                shortname=shortname,
                type='mikrotik',  # specific for Mikrotik
                secret=secret,
                description=description,
                ports=3799, # Default CoA port
                server='localhost', # usually ignored or used for server identification
                community='public', # SNMP community
            )

            self.stdout.write(self.style.SUCCESS(f"Successfully added router: {nas.nasname} (ID: {nas.id})"))
            self.stdout.write(self.style.WARNING("\nIMPORTANT: Make sure to configure the RouterOS side:"))
            self.stdout.write("1. /radius add address=YOUR_SERVER_IP secret=YOUR_SECRET service=hotspot,wireless")
            self.stdout.write("2. /ip hotspot profile set [find] use-radius=yes")

        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR("\nOperation cancelled."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
