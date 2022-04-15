from django.contrib.auth.models import BaseUserManager

from core.infrastructure.choices import ADMIN


class UserManager(BaseUserManager):
    """Manager for Custom User Model"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email Address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.role = ADMIN
        user.is_staff = True
        user.is_superuser = True
        user.is_customer = False
        user.is_gym = False
        user.save(using=self.db)
        return user


