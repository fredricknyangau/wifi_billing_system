from django.db import models

class SiteConfig(models.Model):
    site_name = models.CharField(max_length=100, default="WiFi Billing System")
    maintenance_mode = models.BooleanField(default=False)
    support_email = models.EmailField(blank=True, null=True)
    support_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
