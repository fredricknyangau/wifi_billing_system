from django.contrib import admin
from .models import DataUsage

@admin.register(DataUsage)
class DataUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_start', 'session_end', 'upload_bytes', 'download_bytes')
    list_filter = ('user', 'session_start')
