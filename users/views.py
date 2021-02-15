from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.conf import settings


class LogInView(LoginView):
    template_name = 'users/login.html'
    redirect_field_name = settings.LOGIN_REDIRECT_URL


class SignUpView(TemplateView):
    template_name = 'users/signup.html'