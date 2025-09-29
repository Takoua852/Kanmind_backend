from django.urls import path
from .views import RegistrationView, CustomLoginView, EmailCheckView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),

]