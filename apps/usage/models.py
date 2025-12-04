from django.db import models
from django.conf import settings

class DataUsage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='data_usage')
    session_start = models.DateTimeField()
    session_end = models.DateTimeField(blank=True, null=True)
    upload_bytes = models.BigIntegerField(default=0)
    download_bytes = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.download_bytes} bytes"
