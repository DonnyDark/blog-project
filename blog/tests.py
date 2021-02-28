from django.test import TestCase
from .models import BlogModel, BlogCommentModel
from django.contrib.auth import get_user_model

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

