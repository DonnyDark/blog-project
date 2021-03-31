from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseNotModified, HttpResponse

from .models import BlogModel, BlogCommentModel
from .forms import BlogCreationForm, CommentCreationForm

from texts_and_images.models import TextOrImage
from users.forms import LoginForm


class BlogListView(ListView):
    model = BlogModel
    context_object_name = 'blog_objects'
    template_name = 'blog/main_page.html'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form'] = LoginForm
        return data

    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-published_date')

        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
            queryset = self.model.objects.filter(Q(title__icontains=query))

        if self.request.GET.get('q_tag'):
            tag_query = self.request.GET.get('q_tag')
            queryset = self.model.objects.filter(Q(tags__icontains=tag_query))

        if self.request.user.is_authenticated:
            user = self.request.user
            for query in queryset:
                if query.likes.filter(user=user):
                    query.is_liked = True
                else:
                    query.is_liked = False
                if query.author == user:
                    query.is_author_of_blog = True
                else:
                    query.is_author_of_blog = False
                if query.reposts.filter(username=user.username):
                    query.is_reposted = True
                else:
                    query.is_reposted = False
                query.total_reposts = query.total_reposts()

        for query in queryset:
            if query.tags:
                query.tags_list = query.tags.split(' #')
                for i in range(1, len(query.tags_list)):
                    query.tags_list[i] = '#' + query.tags_list[i]
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

        if obj.tags:
            tags_list = obj.tags.split(' #')
            for i in range(1, len(tags_list)):
                tags_list[i] = '#' + tags_list[1]
            obj.tags_list = tags_list

        if self.request.user.is_authenticated:
            user = self.request.user
            if obj.likes.filter(user=user):
                obj.is_liked = True
            else:
                obj.is_liked = False
            if obj.author == self.request.user:
                obj.is_author_of_blog = True
            else:
                obj.is_author_ob_blog = False
            if obj.reposts.filter(username=user.username):
                obj.is_reposted = True
            else:
                obj.is_reposted = False

        obj.total_reposts = obj.total_reposts()
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data['form'] = LoginForm

        comments = BlogCommentModel.objects.filter(
            blog=self.get_object()).order_by('-date_posted')
        data['comments'] = comments
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentCreationForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            return HttpResponseForbidden()

        if request.POST.get('like'):
            if obj.likes.filter(user=user):
                obj.likes.filter(user=user).delete()
            else:
                obj.likes.create(user=user)
        elif request.POST.get('text'):
            new_comment = BlogCommentModel(text=request.POST.get('text'),
                                           author=user,
                                           blog=self.get_object())
            new_comment.save()
        elif request.POST.get('repost'):
            if obj.author == user:
                return HttpResponse("You can't reposts your own blog!!!")
            else:
                if obj.reposts.filter(username=user.username):
                    obj.reposts.remove(user)
                else:
                    obj.reposts.add(user)

        return self.get(self, request, *args, **kwargs)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogModel
    template_name = 'blog/blog_create.html'
    form_class = BlogCreationForm
    text_or_image_forms = []
    number_of_forms = [0, ]

    def form_invalid(self, form):
        if self.request.POST.get('tags'):
            if '#' not in self.request.POST.get('tags'):
                return super().form_invalid(form)

    def form_valid(self, form):
        request = self.request

        for new_form in self.text_or_image_forms:
            if 'text' in new_form:
                if not request.POST.get(new_form):
                    return self.form_invalid(form)
            elif 'image_url' in new_form:
                if not request.POST.get(new_form):
                    return self.form_invalid(form)

        blog = form.save(commit=False)
        blog.author = self.request.user
        if '#' not in blog.tags:
            blog.tags = '#' + blog.tags
        blog.save()

        for i, new_form in enumerate(self.text_or_image_forms):
            if 'text' in new_form:
                blog.text_or_image.create(text=request.POST.get(new_form), image=None)
            if 'image_url' in new_form:
                url = request.POST.get(new_form)
                image_url = TextOrImage(blog=blog, image_url=url)
                image_url.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.GET.get('text'):
            self.text_or_image_forms.append('text'+str(self.number_of_forms[-1]))
            self.number_of_forms.append(len(self.text_or_image_forms))
        elif request.GET.get('image_url'):
            self.text_or_image_forms.append('image_url'+str(self.number_of_forms[-1]))
            self.number_of_forms.append(len(self.text_or_image_forms))
        elif request.GET.get('delete_form'):
            if not self.text_or_image_forms:
                pass
            else:
                del(self.text_or_image_forms[-1])
                del(self.number_of_forms[-1])
        elif not request.GET.get('text') and not request.GET.get('image_url'):
            del(self.text_or_image_forms[:])
            del(self.number_of_forms[1:])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['body_forms'] = self.text_or_image_forms
        data['number_of_forms'] = self.number_of_forms
        return data


class AboutView(TemplateView):
    template_name = 'blog/about.html'
