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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments = BlogCommentModel.objects.filter(
            blog=self.get_object()).order_by('-date_posted')
        data['comments'] = comments
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentCreationForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = BlogCommentModel(text=request.POST.get('text'),
                                       author=self.request.user,
                                       blog=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogModel
    template_name = 'blog/blog_create.html'
    form_class = BlogCreationForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
