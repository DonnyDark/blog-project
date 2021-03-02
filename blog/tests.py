from django.test import TestCase
from .models import BlogModel, BlogCommentModel
from django.contrib.auth import get_user_model
from .views import BlogListView, BlogDetailView, BlogCreateView, AboutView
from .forms import BlogCreationForm, CommentCreationForm
from django.urls import reverse
from django.test.client import Client

UserModel = get_user_model()


class ModelsTestCase(TestCase):
    def setUp(self):
        UserModel.objects.create(username='User', email='user@example.com', password='UserPass')
        self.user = UserModel.objects.get(username='User')
        BlogModel.objects.create(author=self.user, title='TestTitle', text='TestText')
        blog = BlogModel.objects.get(title='TestTitle')
        BlogCommentModel.objects.create(blog=blog, author=self.user, text='TestComment')

    def test_blog_model_fields(self):
        blog = BlogModel.objects.get(title='TestTitle')
        self.assertEqual(blog.title, 'TestTitle')
        self.assertEqual(blog.author, self.user)
        self.assertEqual(blog.text, 'TestText')
        self.assertEqual(str(blog), f'TestTitle, {self.user.username}')
        self.assertEqual(blog.id, blog.pk)
        self.assertEqual(blog.get_absolute_url(), f'/{str(blog.pk)}/')
        self.assertEqual(blog.number_of_comments, 1)

    def test_blog_comment_model_field(self):
        comment = BlogCommentModel.objects.get(text='TestComment', author=self.user)
        blog = BlogModel.objects.get(title='TestTitle')
        self.assertEqual(comment.text, 'TestComment')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.blog, blog)
        self.assertEqual(str(comment), f"{self.user.username}'s comment for {blog.title}")


class ListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserModel.objects.create(username='User', email='user@example.com', password='UserPass')
        user = UserModel.objects.get(username='User', email='user@example.com', password='UserPass')
        number_of_blogs = 15
        for blog in range(number_of_blogs):
            BlogModel.objects.create(author=user, title=f'TestTitle{blog}', text=f'TestText{blog}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('main_page'))
        self.assertTemplateUsed(response, 'blog/main_page.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('main_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blog_list']) == 10)

    def test_lists_all_blogs(self):
        response = self.client.get(reverse('main_page')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blog_list']) == 5)


class BlogCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        UserModel.objects.create(username='user1', email='user1@example.com', password='user1pass')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('blog_create'))
        self.assertRedirects(response, '/users/login/?next=/create/')

    def test_logged_in_uses_correct_template(self):
        self.client.force_login(UserModel.objects.get_or_create(username='user1')[0])
        response = self.client.get(reverse('blog_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_create.html')

    def test_user_correct_create_new_blog(self):
        login = self.client.login(username='user1', password='user1pass')
        # response = self.client.post()


class BlogCreationAndCommentCreationFormsTestCase(TestCase):
    def setUp(self):
        UserModel.objects.create(username='testuser', email='test@email.com', password='testpass')
        self.user = UserModel.objects.get(username='testuser')
        BlogModel.objects.create(title='test_title', author=self.user, text='test_text')
        self.blog = BlogModel.objects.get(title='test_title')
        BlogCommentModel.objects.create(blog=self.blog, author=self.user, text='test_comment')
        self.comment = BlogCommentModel.objects.get(text='test_comment')

    def test_blog_creation_valid_form(self):
        data = {'title': self.blog.title, 'text': self.blog.text, 'author': self.blog.author}
        form = BlogCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blog_creation_invalid_form(self):
        data = {'title': self.blog.title}
        form = BlogCreationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_comment_creation_valid_form(self):
        data = {'blog': self.comment.blog, 'author': self.comment.author, 'text': self.comment.text}
        form = CommentCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_comment_creation_invalid_form(self):
        data = {}
        form = CommentCreationForm(data=data)
        self.assertFalse(form.is_valid())
