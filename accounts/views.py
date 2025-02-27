from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import CustomUser
import random
import hashlib


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()  # یکسان‌سازی ایمیل
            existing_user = CustomUser.objects.filter(email=email).first()
            if existing_user and existing_user.is_email_verified:
                return render(request, 'accounts/register.html', {'form': form, 'error': 'این ایمیل قبلاً ثبت شده است!'})

            user = form.save(commit=False)
            user.is_active = False  # غیرفعال‌سازی تا تأیید ایمیل

            # تولید و هش کردن کد تأیید ایمیل
            verification_code = f"{random.randint(100000, 999999):06d}"
            hashed_code = hashlib.sha256(
                verification_code.encode()).hexdigest()
            user.email_verification_code = hashed_code
            user.save()

            # ارسال ایمیل تأیید
            send_mail(
                'کد تأیید ایمیل',
                f'کد تأیید شما: {verification_code}',  # ارسال مقدار واقعی
                'mahdiatclash1381@gmail.com',
                [user.email],
                fail_silently=False,
            )

            # ذخیره ایمیل در سشن برای تأیید
            request.session['email'] = user.email
            request.session['attempts'] = 0  # مقدار تلاش برای تأیید

            messages.success(
                request, 'ثبت‌نام موفقیت‌آمیز بود! لطفاً ایمیل خود را بررسی کنید.')
            return redirect('verify_email')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('register')

    attempts = request.session.get('attempts', 0)
    if attempts >= 5:
        return render(request, 'accounts/verify_email.html', {'error': 'تعداد تلاش‌های شما بیش از حد مجاز است. لطفاً دوباره ثبت‌نام کنید.'})

    if request.method == 'POST':
        code = request.POST.get('code')
        hashed_code = hashlib.sha256(code.encode()).hexdigest()

        user = CustomUser.objects.filter(
            email=email, email_verification_code=hashed_code).first()

        if user:
            user.is_email_verified = True
            user.is_active = True
            user.email_verification_code = None  # مقدار را به `None` تغییر دهید
            user.save(update_fields=["is_email_verified",
                      "is_active", "email_verification_code"])
            login(request, user)
            # حذف مقدار تلاش‌ها بعد از تأیید موفق
            request.session.pop('attempts', None)
            return redirect('dashboard')
        else:
            request.session['attempts'] = attempts + 1
            return render(request, 'accounts/verify_email.html', {'error': 'کد اشتباه است'})

    return render(request, 'accounts/verify_email.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user and user.is_email_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'ایمیل شما تأیید نشده است. لطفاً ابتدا ایمیل خود را تأیید کنید.'})
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})
