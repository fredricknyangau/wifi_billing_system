from rest_framework import viewsets, permissions
from .models import DataUsage
from .serializers import DataUsageSerializer

class DataUsageViewSet(viewsets.ModelViewSet):
    serializer_class = DataUsageSerializer
    permission_classes = [permissions.AllowAny] # Import permissions if not already available in file context, but it seems it is not imported in this file. I need to check imports.

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.is_superuser):
            return DataUsage.objects.all()
            
        phone_number = self.request.query_params.get('phone_number')
        if phone_number:
            return DataUsage.objects.filter(user__phone_number=phone_number)
            
        if user.is_authenticated:
            return DataUsage.objects.filter(user=user)
            
        return DataUsage.objects.none()
