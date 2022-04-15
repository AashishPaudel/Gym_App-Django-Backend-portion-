from django.db import models
from django.db.models.signals import post_save
from djmoney.models.fields import MoneyField

from accounts.models import User
from core.infrastructure.choices import ADMIN


class AdminProfile(models.Model):
    """Database model for Admin Profile in the system"""
    
    user = models.OneToOneField(User, related_name="admin_profile", on_delete=models.CASCADE)
    total_earning = MoneyField(max_digits=10, decimal_places=2, default_currency='NPR', default=0.00)
    
    def __str__(self):
        return self.user.name


def add_admin_profile(sender, instance, *args, **kwargs):
    """Function to create admin profile once admin role user is created"""
    if instance.role == ADMIN and not AdminProfile.objects.filter(user=instance).exists():
        AdminProfile.objects.create(user=instance)

post_save.connect(add_admin_profile, sender=User)