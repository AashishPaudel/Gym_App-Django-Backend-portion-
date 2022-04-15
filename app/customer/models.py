from django.db import models
from django.db.models.signals import post_save

from accounts.models import User
from subscription.models import Subscription
from core.infrastructure.choices import CUSTOMER


class CustomerProfile(models.Model):
    """Database model for Customer Profile in the system"""
    
    user = models.OneToOneField(User, related_name="customer_profile", on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    subscription = models.ForeignKey(Subscription, related_name="customer_subscription", on_delete=models.SET_NULL, null=True, blank=True)
    total_check_ins = models.IntegerField(default=0, blank=True)
    remaining_check_ins = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return self.user.name


def add_customer_profile(sender, instance, *args, **kwargs):
    if instance.role == CUSTOMER and not CustomerProfile.objects.filter(user=instance).exists():
        CustomerProfile.objects.create(user=instance)

post_save.connect(add_customer_profile, sender=User)
