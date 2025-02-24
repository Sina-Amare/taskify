from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(
        default=False)  # برای بررسی تأیید ایمیل
    email_verification_code = models.CharField(
        max_length=6, blank=True, null=True)

    def __str__(self):
        return self.username
