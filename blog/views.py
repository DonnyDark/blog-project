from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BlogModel, BlogCommentModel
from .forms import BlogCreationForm, CommentCreationForm


class BlogListView(ListView):
    model = BlogModel
    context_object_name = 'blog_list'
    template_name = 'blog/main_page.html'


class BlogDetailView(DetailView):
    model = BlogModel
    context_object_name = 'blog'
    template_name = 'blog/detail_blog.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogModel
    template_name = 'blog/blog_create.html'
    form_class = BlogCreationForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = BlogCommentModel
    template_name = 'blog/detail_blog.html'
    form_class = CommentCreationForm
