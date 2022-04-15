from django.urls import path, include

from payment.api import viewset


urlpatterns = [
    path('confirm-payment/', viewset.KhaltiPaymentVerificationView.as_view(), name='confirm-payment'),
]