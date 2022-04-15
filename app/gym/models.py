from django.db import models
from django.db.models.signals import post_save
from djmoney.models.fields import MoneyField
from django.core.files.base import ContentFile

import segno
import uuid
import os
import io

from accounts.models import User
from core.infrastructure.choices import GYM
from customer.models import CustomerProfile


class Address(models.Model):
    address = models.CharField(max_length=255)
    district = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=255, blank=True, null=True)
    municipality = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    local_body_name = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(max_length=10, blank=True, null=True)
    longitude = models.FloatField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.address


def get_gym_qr_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join("uploads/qr_codes/", filename)


def get_gym_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join("uploads/gym_images/", filename)


class GymProfile(models.Model):
    """Database model for Gym Profile in the system"""
    
    user = models.OneToOneField(User, related_name="gym_profile", on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=get_gym_image_filename, blank=True, null=True)
    qrcode = models.ImageField(upload_to=get_gym_qr_filename, null=True, blank=True)
    total_earning = MoneyField(max_digits=10, decimal_places=2, default_currency='NPR', default=0.00)
    location = models.ForeignKey(Address, related_name="gym_address", on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        if self.company_name:
            return self.company_name
        return self.user.name


def add_qr_code(instance):
    """Function to save QR code for gym once gym profile is created"""
    qrcode = segno.make(f'http://127.0.0.1:8000/gym/{instance.id}/check-in/')
    out = io.BytesIO()
    qrcode.save(out, kind='png', scale=3)
    instance.qrcode.save(f'gym_{instance.id}.png', ContentFile(out.getvalue()), save=False)
    instance.save()


def add_gym_profile(sender, instance, *args, **kwargs):
    """Function to create gym profile once gym role user is created"""
    if instance.role == GYM and not GymProfile.objects.filter(user=instance).exists():
        gym_profile = GymProfile.objects.create(user=instance)
        add_qr_code(gym_profile)

post_save.connect(add_gym_profile, sender=User)


class CheckIns(models.Model):
    """Database model for Gym Checkins in the system"""
    
    gym = models.ForeignKey(GymProfile, related_name="check_in_gym", on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, related_name="check_in_customer", on_delete=models.CASCADE)
    check_in_at = models.DateTimeField(auto_now_add=True)