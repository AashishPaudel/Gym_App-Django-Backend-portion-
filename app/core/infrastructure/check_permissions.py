from rest_framework import permissions

from core.infrastructure.choices import ADMIN, GYM, CUSTOMER


class UserProfilePermissions(permissions.BasePermission):
    """Only Allow Users to Manage their own Profile"""
    
    def has_object_permission(self, request, view, obj):
        if obj.email == request.user.email:
            return True
        return False


class ProfilePermissions(permissions.BasePermission):
    """Only Allow Profile Users to Manage their own Profile"""
    
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class AdminGymPermissions(permissions.BasePermission):
    """ONly Allow Gyms and Admin"""
    
    def has_permission(self, request, view):
        return request.user.role in [GYM, ADMIN]


class AdminCustomerPermissions(permissions.BasePermission):
    """ONly Allow Customers and Admin"""
    
    def has_permission(self, request, view):
        return request.user.role in [CUSTOMER, ADMIN]


class CustomerPermissions(permissions.BasePermission):
    """ONly Allow Customers"""
    
    def has_permission(self, request, view):
        return request.user.role == CUSTOMER


class GymPermissions(permissions.BasePermission):
    """ONly Allow Gyms"""
    
    def has_permission(self, request, view):
        return request.user.role == GYM


class AdminOnlyUnsafePermissions(permissions.BasePermission):
    """Only Allow Admin to Make Unsafe Permissions"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == ADMIN