from django.shortcuts import render, redirect
from billing.models import Voucher

def portal_login(request):
    """
    The main entry point for the WiFi User.
    MikroTik redirects them here.
    """
    context = {}
    
    # MikroTik sends error messages in the URL (e.g., ?error=invalid_password)
    error_msg = request.GET.get('error')
    if error_msg:
        context['error'] = "Invalid Voucher Code. Please try again."

    return render(request, 'portal/login.html', context)
