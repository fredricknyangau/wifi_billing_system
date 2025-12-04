from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from billing.models import Transaction, Voucher
from usage.models import DataUsage
from django.db.models import Sum

User = get_user_model()

class DashboardStatsView(APIView):
    def get(self, request):
        total_users = User.objects.count()
        total_revenue = Transaction.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
        total_data_usage = DataUsage.objects.aggregate(Sum('download_bytes'))['download_bytes__sum'] or 0
        active_vouchers = Voucher.objects.filter(status='ACTIVE').count()
        
        return Response({
            'total_users': total_users,
            'total_revenue': total_revenue,
            'total_data_usage': total_data_usage,
            'active_vouchers': active_vouchers
        })
