from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import BlogModel, BlogCommentModel
from .forms import BlogCreationForm, CommentCreationForm
from likes.models import Like
from likes.services import add_like, is_fan


class BlogListView(ListView):
    model = BlogModel
    context_object_name = 'blog_objects'
    template_name = 'blog/main_page.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.all()

        if self.request.user.is_authenticated:
            user = self.request.user
            for query in queryset:
                try:
                    query.likes.get(user=user)
                    query.is_liked = True
                except:
                    query.is_liked = False
        return queryset


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


class AboutView(TemplateView):
    template_name = 'blog/about.html'
