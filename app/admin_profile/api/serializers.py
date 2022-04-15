from rest_framework import serializers

from admin_profile.models import AdminProfile


class AdminProfileSerializer(serializers.ModelSerializer):
    """Serializes Gym Profile Object"""
    
    class Meta:
        model = AdminProfile
        fields = "__all__"