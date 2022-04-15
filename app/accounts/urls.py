from django.urls import path, include

from rest_framework.routers import DefaultRouter

from accounts.api import viewset


router = DefaultRouter()
router.register(
    "register-customer", viewset.RegisterUserView, basename="register-customer",
)
router.register(
    "register-gym", viewset.RegisterGymView, basename="register-gym"
)
router.register(
    "profile", viewset.UserProfileView, basename="profile"
)


urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include('djoser.urls.jwt')),
    path('forget-password/', viewset.ForgetPasswordView.as_view(), name='forget-password'),
    path('reset-password/', viewset.ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password-form/', viewset.ResetPasswordFormView.as_view(), name='reset-password-form'),
    path('auth/admin/jwt/refresh/', viewset.CustomRefreshView.as_view(), name='custom_refresh_admin_jwt'),
    path('auth/admin/jwt/create/', viewset.CustomAdminLoginView.as_view(), name='custom_admin_jwt'),
    path('auth/gym/jwt/refresh/', viewset.CustomRefreshView.as_view(), name='custom_refresh_gym_jwt'),
    path('auth/gym/jwt/create/', viewset.CustomGymLoginView.as_view(), name='custom_gym_jwt'),
    path('auth/customer/jwt/refresh/', viewset.CustomRefreshView.as_view(), name='custom_refresh_customer_jwt'),
    path('auth/customer/jwt/create/', viewset.CustomCustomerLoginView.as_view(), name='custom_customer_jwt'),
]