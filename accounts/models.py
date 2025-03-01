from django.contrib.auth.models import AbstractUser
from django.db import models
import hashlib
import random
import re


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(
        default=False)  # Email verification status
    email_verification_code = models.CharField(
        max_length=64, blank=True, null=True)
    phone_number = models.CharField(
        max_length=15, blank=True, default="")  # Optional phone number

    def __str__(self):
        return self.username

    def set_verification_code(self):
        """Generates a hashed verification code and stores it in the database."""
        code = f"{random.randint(100000, 999999):06d}"  # 6-digit verification code
        hashed_code = hashlib.sha256(code.encode()).hexdigest()
        self.email_verification_code = hashed_code
        self.save(update_fields=["email_verification_code"])
        return code  # The actual code to be sent via email

    def is_valid_phone_number(self):
        """Validates phone number format for Iranian numbers."""
        return bool(re.match(r'^\+98\d{10}$', self.phone_number))
