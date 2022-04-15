from dataclasses import field
from rest_framework import serializers

from customer.api.serializers import CustomerProfileSerializer
from gym.models import GymProfile, Address, CheckIns


class AddressSerializer(serializers.ModelSerializer):
    """Serializes Gym Address Object"""
    
    class Meta:
        model = Address
        fields = "__all__"
    
    def validate(self, attrs):
        latitude = attrs.get("latitude", None)
        longitude = attrs.get("longitude", None)
        if not latitude or not longitude:
            raise serializers.ValidationError("Latitude and Longitude cannot be null", 400)
        return super().validate(attrs)


class GymProfileSerializer(serializers.ModelSerializer):
    """Serializes Gym Profile Object"""
    address_detail = serializers.SerializerMethodField('get_address_detail')
    
    def get_address_detail(self, obj):
        if obj.location:
            return AddressSerializer(obj.location).data
        return None
    
    class Meta:
        model = GymProfile
        fields = "__all__"
        read_only_fields = ("user", "total_earning", "qrcode")
        extra_fields = ("address_detail")


class AllGymSerializer(serializers.ModelSerializer):
    """Serializes Gym Profile Object"""
    location = AddressSerializer()
    location_map = serializers.SerializerMethodField('get_location_map')
    
    def get_location_map(self, obj):
        if obj.location:
            location_link = f"https://www.google.com/maps/search/?api=1&query={obj.location.latitude}%2C{obj.location.longitude}"
            return location_link
        return None
    
    class Meta:
        model = GymProfile
        fields = [
            "id",
            "company_name",
            "description",
            "image",
            "qrcode",
            "location",
            "location_map"
        ]


class CheckInsSerializer(serializers.ModelSerializer):
    """Serializes User Gym Check In Data"""
    gym = GymProfileSerializer()
    customer = CustomerProfileSerializer()
    customer_name = serializers.SerializerMethodField('get_customer_name')
    gym_name = serializers.SerializerMethodField('get_gym_name')
    
    def get_customer_name(self, obj):
        return obj.customer.user.name
    
    def get_gym_name(self, obj):
        return obj.gym.user.name
    
    class Meta:
        model = CheckIns
        fields = "__all__"