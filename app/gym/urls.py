from django.urls import path, include

from rest_framework.routers import DefaultRouter

from gym.api import viewset


router = DefaultRouter()
router.register(
    "all-gyms", viewset.AllGymViewSet, basename="all-gyms"
)
router.register(
    "profile", viewset.GymProfileViewSet, basename="profile"
)
router.register(
    "address", viewset.AddressViewSet, basename="address"
)
router.register(
    "all-check-ins", viewset.CheckInsViewSet, basename="all-check-ins"
)

urlpatterns = [
    path("", include(router.urls)),
    path('<int:gymprofile_id>/check-in/', viewset.GymCheckInView.as_view()),
]