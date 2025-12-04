from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API V1
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/customers/', include('customers.urls')),
    path('api/v1/billing/', include('billing.urls')),
    path('api/v1/usage/', include('usage.urls')),
    path('api/v1/reports/', include('reports.urls')),
    path('api/v1/radius/', include('radius.urls')),
    path('api/v1/analytics/', include('analytics.urls')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)