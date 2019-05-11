from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    is_verified = models.BooleanField(default=True)
    public_name = models.CharField(max_length=130, null=True, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    city = models.CharField(max_length=130, blank=True)

    def __str__(self):
        return self.public_name
