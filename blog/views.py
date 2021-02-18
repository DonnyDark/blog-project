from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BlogModel
from .forms import BlogForm


class BlogListView(ListView):
    model = BlogModel
    context_object_name = 'blog_list'
    template_name = 'blog/main_page.html'


class BlogDetailView(DetailView):
    model = BlogModel


class BlogCreateView(LoginRequiredMixin, CreateView):
    models = BlogModel
    template_name = 'blog/blog_create.html'
    form_class = BlogForm
