from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChurnPredictionViewSet, CustomerHealthScoreViewSet

router = DefaultRouter()
router.register(r'churn-predictions', ChurnPredictionViewSet)
router.register(r'health-scores', CustomerHealthScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
