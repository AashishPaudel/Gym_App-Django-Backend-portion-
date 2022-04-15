from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

import random

from accounts.api import serializers
from accounts import models
from core.infrastructure import choices
from core.infrastructure.check_permissions import UserProfilePermissions


class RegisterUserView(viewsets.ModelViewSet):
    """API Views for Registering Users in the System"""
    
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]
    
    def perform_create(self, serializer):
        serializer.save(role=choices.CUSTOMER)


class RegisterGymView(viewsets.ModelViewSet):
    """API Views for Registering Gym in the System"""
    
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    http_method_names = ["post"]
    
    def perform_create(self, serializer):
        serializer.save(role=choices.GYM)


class UserProfileView(viewsets.ModelViewSet):
    """API Views for Handling User Profile in the System"""
    
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated, UserProfilePermissions,)
    http_method_names = ["get","put","patch","delete"]
    
    def get_queryset(self):
        return models.User.objects.filter(email=self.request.user.email)


class ForgetPasswordView(APIView):
    """API View for Forget Password"""
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        # getting email from request body
        email = self.request.data.get("email", None)
        # validating if user has entered email and email for registered user exists
        if email and models.User.objects.filter(email=email).exists():
            OTP = str(random.randint(111111, 999999))
            # creating token in database for user
            models.UserToken.objects.create(email=email,otp=OTP)
            # returning success response to the user
            return Response("Password reset link sent successfully. Please check email", status=status.HTTP_200_OK)
        else:
            # returning error response to the user if email is not entered or does not exist
            return Response("Please enter registered email", status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """API View for resetting password"""
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        # getting otp from url
        otp = self.request.query_params.get("otp", None)
        user_token = models.UserToken.objects.filter(otp=otp).first()
        # validating if otp exists
        if user_token:
            user = models.User.objects.get(email=user_token.email)
            # getting password and confirm password from request body
            password = self.request.data.get("password", None)
            confirm_password = self.request.data.get("confirm_password", None)
            # changing password if both match
            if password == confirm_password:
                user.set_password(password)
                user.save()
                return Response("Password changed successfully.", status=status.HTTP_200_OK)
            else:
                return Response("Password and Confirm Password do not match", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("OTP Incorrect Please Try Again", status=status.HTTP_400_BAD_REQUEST)


class CustomAdminLoginView(TokenObtainPairView):
    
    serializer_class = serializers.CustomAdminOnlyJWTToken


class CustomGymLoginView(TokenObtainPairView):
    
    serializer_class = serializers.CustomGymOnlyJWTToken


class CustomCustomerLoginView(TokenObtainPairView):
    
    serializer_class = serializers.CustomCustomerOnlyJWTToken


class CustomRefreshView(TokenObtainPairView):
    
    serializer_class = serializers.CustomRefreshJWTToken


class ResetPasswordFormView(APIView):
    """API View for resetting password"""
    permission_classes = (AllowAny,)
    
    def post(self, request, format=None):
        # getting otp from form data
        otp = self.request.data.get("otp", None)
        user_token = models.UserToken.objects.filter(otp=otp).first()
        # validating if otp exists
        if user_token:
            user = models.User.objects.get(email=user_token.email)
            # getting password and confirm password from request body
            password = self.request.data.get("password", None)
            confirm_password = self.request.data.get("confirm_password", None)
            # changing password if both match
            if password == confirm_password:
                user.set_password(password)
                user.save()
                return Response("Password changed successfully.", status=status.HTTP_200_OK)
            else:
                return Response("Password and Confirm Password do not match", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("OTP Incorrect Please Try Again", status=status.HTTP_400_BAD_REQUEST)