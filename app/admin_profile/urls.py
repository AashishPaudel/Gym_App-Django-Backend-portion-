from django.urls import path, include

from rest_framework.routers import DefaultRouter

from admin_profile.api import viewset


router = DefaultRouter()
router.register(
    "", viewset.AdminProfileViewSet, basename=""
)

urlpatterns = [
    path("", include(router.urls)),
]