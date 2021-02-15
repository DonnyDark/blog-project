from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from .forms import MyAuthenticationForm


class LogInView(LoginView):
    template_name = 'users/login.html'
    authentication_form = MyAuthenticationForm



class SignUpView(TemplateView):
    template_name = 'users/signup.html'