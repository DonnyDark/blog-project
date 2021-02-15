from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'users/sign_up.html'