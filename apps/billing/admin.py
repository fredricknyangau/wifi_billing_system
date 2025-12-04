from django.contrib import admin
from .models import PricingPlan, Voucher, Transaction

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_minutes', 'speed_limit')

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'plan', 'status', 'created_at')
    list_filter = ('status', 'plan')
    search_fields = ('code',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'phone_number', 'amount', 'status', 'transaction_date')
    search_fields = ('receipt_number', 'phone_number')
