from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'blog/main_page.html'