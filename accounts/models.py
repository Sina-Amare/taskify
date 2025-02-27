from django.contrib.auth.models import AbstractUser
from django.db import models
import hashlib
import random


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)  # بررسی تأیید ایمیل
    email_verification_code = models.CharField(
        max_length=64, blank=True, null=True)

    def __str__(self):
        return self.username

    def set_verification_code(self):
        code = f"{random.randint(100000, 999999):06d}"  # تضمین ۶ رقمی بودن کد
        hashed_code = hashlib.sha256(code.encode()).hexdigest()
        self.email_verification_code = hashed_code
        # ذخیره مقدار هش شده
        self.save(update_fields=["email_verification_code"])
        return code  # مقدار واقعی برای ارسال ایمیل
