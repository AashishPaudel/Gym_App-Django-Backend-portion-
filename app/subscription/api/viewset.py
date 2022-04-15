from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from subscription.api import serializers
from subscription import models
from core.infrastructure.check_permissions import AdminOnlyUnsafePermissions

class SubscriptionViewSet(viewsets.ModelViewSet):
    """API Views for Handling Subscription in the System"""
    
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = (IsAuthenticated, AdminOnlyUnsafePermissions)
