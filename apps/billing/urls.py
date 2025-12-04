from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from .views import PricingPlanViewSet, VoucherViewSet, TransactionViewSet, MpesaPaymentView, MpesaCallbackView

router = DefaultRouter()
router.register(r'plans', PricingPlanViewSet)
router.register(r'vouchers', VoucherViewSet)
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('mpesa/pay', MpesaPaymentView.as_view(), name='mpesa-pay'),
    path('mpesa/callback', csrf_exempt(MpesaCallbackView.as_view()), name='mpesa-callback'),
]