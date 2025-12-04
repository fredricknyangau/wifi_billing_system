from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import PricingPlan, Voucher, Transaction
from .serializers import PricingPlanSerializer, VoucherSerializer, TransactionSerializer
from .mpesa import MpesaClient
import logging
import uuid
import random

logger = logging.getLogger(__name__)

class PricingPlanViewSet(viewsets.ModelViewSet):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer
    permission_classes = [permissions.AllowAny] # Change to IsAuthenticated in production

class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        # Allow filtering by phone number for the frontend to poll status
        phone_number = self.request.query_params.get('phone_number')
        if phone_number:
            return Transaction.objects.filter(phone_number=phone_number).order_by('-transaction_date')
        return Transaction.objects.none()


@method_decorator(csrf_exempt, name='dispatch')
class MpesaPaymentView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')
        
        if not phone_number or not amount:
            return Response({'error': 'Phone number and amount required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            client = MpesaClient()
            # Reference for internal tracking (temporary)
            temp_ref = f"WS{uuid.uuid4().hex[:8].upper()}"
            
            # Initiate STK Push
            response = client.stk_push(phone_number, amount, account_reference=temp_ref)
            
            # Extract the Critical ID
            checkout_req_id = response.get('CheckoutRequestID')

            if response.get('ResponseCode') == '0':
                # Save transaction with the ID Safaricom gave us
                Transaction.objects.create(
                    checkout_request_id=checkout_req_id,
                    phone_number=phone_number,
                    amount=amount,
                    status='Pending'
                )
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"M-Pesa Error: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info(f"M-Pesa Callback: {request.data}")
        
        try:
            body = request.data.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            checkout_req_id = stk_callback.get('CheckoutRequestID')
            
            # 1. Match the Transaction using the ID
            transaction = Transaction.objects.filter(checkout_request_id=checkout_req_id).first()

            if not transaction:
                logger.error(f"Transaction not found for ID: {checkout_req_id}")
                return Response({'status': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

            if result_code == 0:
                # Payment Successful
                meta = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                receipt = next((i['Value'] for i in meta if i['Name'] == 'MpesaReceiptNumber'), None)
                
                # Update Transaction
                transaction.status = 'Completed'
                transaction.receipt_number = receipt
                transaction.save()

                # --- VOUCHER GENERATION LOGIC ---
                # Find the plan that matches this amount
                plan = PricingPlan.objects.filter(price=transaction.amount).first()
                
                if plan:
                    # Generate Code
                    code = str(random.randint(100000, 999999))
                    # Create Voucher (Radius sync happens in models.py)
                    Voucher.objects.create(code=code, plan=plan)
                    print(f"✅ VOUCHER GENERATED: {code} for {transaction.phone_number}")
                    # TODO: Call SMS Service here
                else:
                    logger.warning(f"No plan found for amount: {transaction.amount}")

            else:
                # Payment Failed/Cancelled
                transaction.status = 'Failed'
                transaction.save()

            return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Callback Error: {str(e)}")
            return Response