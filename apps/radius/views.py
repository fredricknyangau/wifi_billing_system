from rest_framework import viewsets
from .models import Nas, Radcheck, Radreply, Radacct, Radusergroup, Radgroupreply, Radgroupcheck
from .serializers import (
    NasSerializer, RadcheckSerializer, RadreplySerializer, RadacctSerializer,
    RadusergroupSerializer, RadgroupreplySerializer, RadgroupcheckSerializer
)

class NasViewSet(viewsets.ModelViewSet):
    queryset = Nas.objects.all()
    serializer_class = NasSerializer

class RadcheckViewSet(viewsets.ModelViewSet):
    queryset = Radcheck.objects.all()
    serializer_class = RadcheckSerializer

class RadreplyViewSet(viewsets.ModelViewSet):
    queryset = Radreply.objects.all()
    serializer_class = RadreplySerializer

class RadacctViewSet(viewsets.ModelViewSet):
    queryset = Radacct.objects.all()
    serializer_class = RadacctSerializer

class RadusergroupViewSet(viewsets.ModelViewSet):
    queryset = Radusergroup.objects.all()
    serializer_class = RadusergroupSerializer

class RadgroupreplyViewSet(viewsets.ModelViewSet):
    queryset = Radgroupreply.objects.all()
    serializer_class = RadgroupreplySerializer

class RadgroupcheckViewSet(viewsets.ModelViewSet):
    queryset = Radgroupcheck.objects.all()
    serializer_class = RadgroupcheckSerializer
