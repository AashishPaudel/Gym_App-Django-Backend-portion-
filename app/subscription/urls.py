from django.urls import path, include

from rest_framework.routers import DefaultRouter

from subscription.api import viewset


router = DefaultRouter()
router.register(
    "subscription", viewset.SubscriptionViewSet, basename="subscription"
)


urlpatterns = [
    path("", include(router.urls)),
]