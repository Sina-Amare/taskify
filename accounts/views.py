from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm, LoginForm
from .models import CustomUser
import random
from django.core.mail import send_mail


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # تا زمانی که ایمیل تأیید نشه، کاربر غیرفعال می‌مونه
            user.email_verification_code = str(random.randint(100000, 999999))
            user.save()

            # ارسال ایمیل تأیید
            send_mail(
                'کد تأیید ایمیل',
                f'کد تأیید شما: {user.email_verification_code}',
                'no-reply@example.com',
                [user.email],
                fail_silently=False,
            )

            # ذخیره ایمیل در سشن برای تأیید
            request.session['email'] = user.email
            return redirect('verify_email')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('register')

    if request.method == 'POST':
        code = request.POST.get('code')
        user = CustomUser.objects.filter(
            email=email, email_verification_code=code).first()

        if user:
            user.is_email_verified = True
            user.is_active = True
            user.email_verification_code = ''
            user.save()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/verify_email.html', {'error': 'کد اشتباه است'})

    return render(request, 'accounts/verify_email.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.is_email_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'ایمیل شما تأیید نشده است'})
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})
