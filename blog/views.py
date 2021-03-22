from django.shortcuts import redirect
from django.http import HttpResponseNotModified, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from .models import BlogModel, BlogCommentModel
from .forms import BlogCreationForm, CommentCreationForm

from texts_and_images.forms import TextCreationForm, ImageCreationForm
from texts_and_images.models import TextOrImage


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
    number_of_forms = [0, ]

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user
        blog.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.GET.get('text'):
            self.text_or_image_forms.append('text'+str(self.number_of_forms[-1]))
            self.number_of_forms.append(len(self.text_or_image_forms))
        elif request.GET.get('image'):
            self.text_or_image_forms.append('image'+str(self.number_of_forms[-1]))
            self.number_of_forms.append(len(self.text_or_image_forms))
        elif request.GET.get('delete_form'):
            if not self.text_or_image_forms:
                pass
            else:
                del(self.text_or_image_forms[-1])
                del(self.number_of_forms[-1])
        elif not request.GET.get('text') and not request.GET.get('image'):
            del(self.text_or_image_forms[:])
            del(self.number_of_forms[1:])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['body_forms'] = self.text_or_image_forms
        data['number_of_forms'] = self.number_of_forms
        return data

    def post(self, request, *args, **kwargs):
        texts = []
        if request.POST.get('text'):
            for i in range(len(request.POST.get('text'))):
                if request.POST.get('text')[i] == '':
                    return HttpResponseNotModified
                else:
                    texts.append(request.POST.get('text')[i])
        images = []
        if request.POST.get('image'):
            for image in request.POST.get('image'):
                if image == '':
                    return HttpResponseNotModified
                else:
                    images.append(image)

        if self.text_or_image_forms:
            for form in self.text_or_image_forms:
                if form == TextCreationForm:
                    new_text = TextOrImage(blog=self.get_object(), text=texts[0], image=None)
                    new_text.save()
                    del(texts[0])
                if form == ImageCreationForm:
                    new_image = TextOrImage(blog=self.get_object(), image=image[0], text=None)
                    new_image.save()
                    del(image[0])

        return super().post(request, *args, **kwargs)


class AboutView(TemplateView):
    template_name = 'blog/about.html'
