"""
Authentication API Endpoints.

1. /registration/  - POST: Register a new user
2. /login/         - POST: Login with email and password
"""

from django.urls import path
from .views import RegistrationView, CustomLoginView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", CustomLoginView.as_view(), name="login"),
]
