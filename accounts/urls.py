from django.urls import path
from .views import register_view, verify_email_view, login_view, dashboard_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('verify-email/', verify_email_view, name='verify_email'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
