from django.contrib.auth import views as auth_views
from django.views import generic
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, RegisterForm

from blog.models import BlogModel


UserModel = get_user_model()


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'


class SignupView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('login')


class UserView(LoginRequiredMixin, generic.DetailView):
    template_name = 'users/user.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        user = UserModel.objects.get(username=self.request.user.username)
        return user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        user_blogs = BlogModel.objects.filter(author=self.get_object())
        data['user_blogs'] = user_blogs
        data['queryset'] = self.get_queryset()
        if self.request.GET.get('q'):
            if self.request.GET.get('q') == 'user_reposts':
                data['blogs'] = 'user_reposts'
            elif self.request.GET.get('q') == 'user_blogs':
                data['blogs'] = 'user_blogs'
        return data

    def get_queryset(self):
        if self.request.GET.get('q'):
            if self.request.GET.get('q') == 'user_reposts':
                queryset = self.get_object().reposts.all()
            elif self.request.GET.get('q') == 'user_blogs':
                queryset = BlogModel.objects.filter(author=self.get_object())
            else:
                queryset = None

            if queryset:
                for query in queryset:
                    if query.reposts.filter(username=self.get_object().username):
                        query.is_reposted = True
                    else:
                        query.is_reposted = False
            return queryset