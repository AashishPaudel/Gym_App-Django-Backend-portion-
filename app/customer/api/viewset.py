from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from customer.api import serializers
from customer import models
from core.infrastructure.check_permissions import ProfilePermissions, CustomerPermissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """API Views for Handling User Profile in the System"""
    
    serializer_class = serializers.CustomerProfileSerializer
    permission_classes = (IsAuthenticated, ProfilePermissions, CustomerPermissions)
    http_method_names = ["get","put","patch"]
    
    def get_queryset(self):
        return models.CustomerProfile.objects.filter(user=self.request.user)


class CustomerSubscriptionViewSet(viewsets.ModelViewSet):
    """API Views for Handling User Profile in the System"""
    
    serializer_class = serializers.CustomerSubscriptionSerializer
    permission_classes = (IsAuthenticated, ProfilePermissions, CustomerPermissions)
    http_method_names = ["get","patch"]
    
    def get_queryset(self):
        return models.CustomerProfile.objects.filter(user=self.request.user)