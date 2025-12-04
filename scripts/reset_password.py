import os
import django
import sys

sys.path.append('/home/fred/Projects/wifi-billing-system')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from accounts.models import User

def reset_password():
    username = "admin"
    password = "password123"
    
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"✅ Password for '{username}' has been reset to '{password}'.")
    except User.DoesNotExist:
        print(f"⚠️ User '{username}' not found. Creating new superuser.")
        User.objects.create_superuser(username=username, email="admin@example.com", password=password)
        print(f"✅ Superuser '{username}' created with password '{password}'.")

if __name__ == "__main__":
    reset_password()
