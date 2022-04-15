from decimal import Decimal
from django.db.models.signals import pre_save
from django.db import models
from djmoney.models.fields import MoneyField

import uuid
import os


def get_subscription_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join("media/uploads/subscription_images/", filename)


class Subscription(models.Model):
    """Database model for Subscription in the system"""
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    valid_for = models.IntegerField()
    image = models.ImageField(upload_to=get_subscription_image_filename, blank=True, null=True)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='NPR')
    per_day_price = MoneyField(max_digits=10, decimal_places=2, default_currency='NPR', blank=True, null=True)
    
    def __str__(self):
        return self.name


def calculate_per_day_price(sender, instance, *args, **kwargs):
    instance.per_day_price = instance.price.amount/Decimal(instance.valid_for)

pre_save.connect(calculate_per_day_price, sender=Subscription)
