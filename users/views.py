from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'


class SignupView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')


class UserView(generic.DetailView):
    template_name = 'users/user.html'
    context_object_name = 'user'
