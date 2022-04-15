from django.urls import path, include

from rest_framework.routers import DefaultRouter

from customer.api import viewset


router = DefaultRouter()
router.register(
    "profile", viewset.UserProfileViewSet, basename="profile"
)
router.register(
    "subscribe", viewset.CustomerSubscriptionViewSet, basename="subscribe"
)


urlpatterns = [
    path("", include(router.urls)),
]