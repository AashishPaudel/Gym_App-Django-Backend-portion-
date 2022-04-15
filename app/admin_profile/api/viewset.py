from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from admin_profile.api import serializers
from admin_profile.models import AdminProfile


class AdminProfileViewSet(viewsets.ModelViewSet):
    """API Views for Handling Admin Profile in the System"""
    
    serializer_class = serializers.AdminProfileSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    http_method_names = ["get",]
    
    def get_queryset(self):
        return AdminProfile.objects.filter(user=self.request.user)