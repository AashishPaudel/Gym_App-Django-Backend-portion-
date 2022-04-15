
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from core.infrastructure.choices import ADMIN, GYM, CUSTOMER
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User database object"""

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "name",
            "address",
            "gender",
            "phone",
            "password",
            "image",
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ("id",)
    
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class CustomRefreshJWTToken(TokenRefreshSerializer):
    
    def validate(self,attrs):
        data = super().validate(attrs)
        if not RefreshToken(attrs['refresh']):
            raise serializers.ValidationError("Refresh token is undefined", 405)
        user_id = RefreshToken(attrs['refresh']).access_token['user_id']
        if user_id:
            user = User.objects.get(pk=user_id)
            data['user_id'] = user.id
            data['name'] = user.name
            if user.role == ADMIN:
                data['admin_id'] = user.admin_profile.id
            elif user.role == GYM:
                data['gym_profile_id'] = user.gym_profile.id
            else:
                data['customer_profile_id'] = user.customer_profile.id
        return data


class CustomAdminOnlyJWTToken(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != ADMIN:
            raise serializers.ValidationError("Only Admin is Allowed to Login Here", 405)
        data['user_id'] = self.user.id
        data['name'] = self.user.name
        data['admin_id'] = self.user.admin_profile.id
        return data


class CustomCustomerOnlyJWTToken(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != CUSTOMER:
            raise serializers.ValidationError("Only Customer is Allowed to Login Here", 405)
        data['user_id'] = self.user.id
        data['name'] = self.user.name
        data['customer_id'] = self.user.customer_profile.id
        return data


class CustomGymOnlyJWTToken(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.role != GYM:
            raise serializers.ValidationError("Only Gym is Allowed to Login Here", 405)
        data['user_id'] = self.user.id
        data['name'] = self.user.name
        data['gym_profile_id'] = self.user.gym_profile.id
        return data