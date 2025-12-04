import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

try:
    from customers.models import Customer
    print("Successfully imported Customer from customers.models")
except Exception as e:
    print(f"Failed to import Customer: {e}")
    sys.exit(1)
