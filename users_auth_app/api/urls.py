from django.urls import path
from .views import RegistrationView, LoginView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login")
]