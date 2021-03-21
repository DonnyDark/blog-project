from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from .models import BlogModel, BlogCommentModel
from .forms import BlogCreationForm, CommentCreationForm

from texts_and_images.forms import TextCreationForm, ImageCreationForm


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
                if query.likes.filter(user=user):
                    query.is_liked = True
                else:
                    query.is_liked = False
        return queryset


class BlogDetailView(DetailView):
    model = BlogModel
    context_object_name = 'blog'
    template_name = 'blog/detail_blog.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            obj = self.model.objects.get(id=self.get_object().id)
            obj.views += 1
            obj.save()
        return super().get(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_authenticated:
            user = self.request.user
            if obj.likes.filter(user=user):
                obj.is_liked = True
            else:
                obj.is_liked = False
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments = BlogCommentModel.objects.filter(
            blog=self.get_object()).order_by('-date_posted')
        data['comments'] = comments
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentCreationForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.POST.get('like'):
            if self.request.user.is_authenticated:
                user = self.request.user
                if obj.likes.filter(user=user):
                    obj.likes.filter(user=user).delete()
                else:
                    obj.likes.create(user=user)
            else:
                return HttpResponseForbidden
        elif request.POST.get('text'):
            new_comment = BlogCommentModel(text=request.POST.get('text'),
                                           author=self.request.user,
                                           blog=self.get_object())
            new_comment.save()
        return self.get(self, request, *args, **kwargs)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogModel
    template_name = 'blog/blog_create.html'
    form_class = BlogCreationForm
    text_or_image_forms = []

    def get(self, request, *args, **kwargs):
        if request.GET.get('text'):
            self.text_or_image_forms.append(TextCreationForm())
        elif request.GET.get('image'):
            self.text_or_image_forms.append(ImageCreationForm())
        elif not request.GET.get('text') and not request.GET.get('image'):
            del(self.text_or_image_forms[:])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['body_forms'] = self.text_or_image_forms
        return data


class AboutView(TemplateView):
    template_name = 'blog/about.html'
