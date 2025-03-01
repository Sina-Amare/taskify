from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
import re


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 6:
            raise forms.ValidationError(
                "Username must be at least 6 characters long.")
        return username

    def clean_password1(self):
        """Ensures the password contains at least one uppercase letter and one special character."""
        password = self.cleaned_data.get('password1')
        if not re.search(r'[A-Z]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter (A-Z) and one special character (!@#$%^&*...)."
            )
        return password

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email:", widget=forms.TextInput(attrs={"autofocus": True})
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form to update user profile including phone number validation."""
    phone_number = forms.CharField(required=False)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number", "").strip()

        # بررسی فرمت شماره ایران
        if phone_number and not re.match(r'^(\+98|0)9\d{9}$', phone_number):
            raise forms.ValidationError(
                "Phone number must be a valid Iranian number (e.g., +989123456789 or 09123456789)."
            )

        # تبدیل شماره به فرمت استاندارد (+98XXXXXXXXXX)
        if phone_number.startswith("0"):
            phone_number = "+98" + phone_number[1:]

        # بررسی اینکه شماره از قبل در دیتابیس نباشد (به جز برای کاربر فعلی)
        existing_user = CustomUser.objects.filter(
            phone_number=phone_number).exclude(pk=self.instance.pk).first()
        if existing_user:
            raise forms.ValidationError(
                "This phone number is already in use by another user.")

        return phone_number

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']
