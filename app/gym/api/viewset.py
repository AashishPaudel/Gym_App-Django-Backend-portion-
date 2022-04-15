from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from decimal import Decimal
from core.infrastructure.choices import CUSTOMER, GYM

from gym.api import serializers
from gym import models
from core.infrastructure.check_permissions import ProfilePermissions, GymPermissions, AdminGymPermissions, CustomerPermissions
from admin_profile.models import AdminProfile


class AddressViewSet(viewsets.ModelViewSet):
    """API Views for Handling  Gym Address in the System"""
    
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = (IsAuthenticated, AdminGymPermissions)


class AllGymViewSet(viewsets.ModelViewSet):
    """API Views for Handling Gym Profile in the System"""
    
    queryset = models.GymProfile.objects.all()
    serializer_class = serializers.AllGymSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]


class GymProfileViewSet(viewsets.ModelViewSet):
    """API Views for Handling Gym Profile in the System"""
    
    serializer_class = serializers.GymProfileSerializer
    permission_classes = (IsAuthenticated, ProfilePermissions, GymPermissions)
    http_method_names = ["get","put","patch"]
    
    def get_queryset(self):
        return models.GymProfile.objects.filter(user=self.request.user)


class GymCheckInView(APIView):
    """API View for Handling Gym Check Ins in the System"""
    permission_classes = (IsAuthenticated, CustomerPermissions)
    
    def post(self, request,gymprofile_id, format=None):
        # getting gym profile and customer profile
        gym = models.GymProfile.objects.get(id=gymprofile_id)
        customer = self.request.user.customer_profile
        
        if customer.subscription and customer.remaining_check_ins > 0:
            # adding amount to gym after user enters gym
            per_day_amount = customer.subscription.per_day_price.amount
            gym.total_earning.amount += per_day_amount * Decimal(0.8)
            
            # adding amount to admin after user enters gym
            admin = AdminProfile.objects.all().first()
            admin.total_earning.amount += per_day_amount * Decimal(0.2)
            
            # subtracting remaining days from user
            customer.remaining_check_ins -= 1
            customer.total_check_ins += 1
            
            # saving updated objects
            admin.save()
            gym.save()
            customer.save()
            
            # creating gym checkin after user checkins
            models.CheckIns.objects.create(gym=gym,customer=customer)
            
            # Returning response to user
            return Response("Please Enjoy Your Time In Gym", status=status.HTTP_200_OK)
        else:
            return Response("You do not have any subscriptions", status=status.HTTP_401_UNAUTHORIZED)


class CheckInsViewSet(viewsets.ModelViewSet):
    """API Views for Handling Gym CheckIns in the System"""
    
    serializer_class = serializers.CheckInsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]
    
    def get_queryset(self):
        if self.request.user.role == GYM:
            # returning all checkins in the gym for requesting gym user
            return models.CheckIns.objects.filter(gym=self.request.user.gym_profile)
        if self.request.user.role == CUSTOMER:
            # returning all check ins made by customer for himself
            return models.CheckIns.objects.filter(customer=self.request.user.customer_profile)
        return models.CheckIns.objects.all()
