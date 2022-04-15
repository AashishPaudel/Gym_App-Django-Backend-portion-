from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

import uuid
import os

from accounts.api.managers import UserManager
from core.infrastructure import choices
from core.settings import EMAIL_HOST_USER


def get_user_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join("uploads/user_images/", filename)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    gender = models.CharField(
        choices=choices.GENDER_TYPES, max_length=10, default=choices.MALE
    )
    image = models.ImageField(upload_to=get_user_image_filename, blank=True, null=True)
    role = models.CharField(
        choices=choices.PROFILE_TYPES, max_length=15, default=choices.ADMIN
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_gym = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class UserToken(models.Model):
    """Database Table for User Tokens Generated to Reset Password"""
    
    email = models.EmailField(max_length=255)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.user.email


def send_password_reset_email(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'RESET PASSWORD'
        message = f'OTP = {instance.otp}'
        from_email = EMAIL_HOST_USER
        to_email = [instance.email]
        send_mail(subject,message,from_email,to_email)

post_save.connect(send_password_reset_email, sender=UserToken)