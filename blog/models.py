import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

from likes.models import Like

UserModel = get_user_model()


class BlogModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now, editable=True)
    # tags = models.CharField()
    likes = GenericRelation(Like)

    def __str__(self):
        return self.title + ', ' + self.author.username

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

    @property
    def number_of_comments(self):
        return BlogCommentModel.objects.filter(blog=self).count()

    @property
    def total_likes(self):
        return self.likes.count()


class BlogCommentModel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False, editable=True)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.author.username) + "'s comment for " + self.blog.title


