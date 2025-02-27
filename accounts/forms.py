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
                "نام کاربری باید حداقل ۶ کاراکتر باشد.")
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.search(r'[A-Z]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError(
                "رمز عبور باید حداقل یک حرف بزرگ (A-Z) داشته باشد. ,ر خاص(!@  # $%^&*...) داشته باشد.")
        return password

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="ایمیل یا نام کاربری", widget=forms.TextInput(attrs={"autofocus": True})
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
