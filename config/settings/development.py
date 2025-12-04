from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True # Development only

# --- CORS & SECURITY SETTINGS ---
# Allow all origins for development and explicitly list localhost ports
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    # Add the IP address of your server running the React App (if external device is testing)
    # E.g., "http://192.168.88.254:5173" 
]

# Ensure Django accepts requests directed at localhost and your server IP
ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost', 
    '192.168.88.254', # My Server IP
]

# CSRF trusted origins for POST/PUT/DELETE requests from frontend
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://192.168.88.254:5173",
    "http://192.168.88.254:5174",
]