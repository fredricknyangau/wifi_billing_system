from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NasViewSet, RadcheckViewSet, RadreplyViewSet, RadacctViewSet,
    RadusergroupViewSet, RadgroupreplyViewSet, RadgroupcheckViewSet
)

router = DefaultRouter()
router.register(r'nas', NasViewSet)
router.register(r'radcheck', RadcheckViewSet)
router.register(r'radreply', RadreplyViewSet)
router.register(r'radacct', RadacctViewSet)
router.register(r'radusergroup', RadusergroupViewSet)
router.register(r'radgroupreply', RadgroupreplyViewSet)
router.register(r'radgroupcheck', RadgroupcheckViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
