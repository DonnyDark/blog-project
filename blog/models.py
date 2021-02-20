import uuid
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class BlogModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    published_date = models.DateTimeField(default=timezone.now, editable=True)
    liked = models.IntegerField(editable=True, blank=True, null=True)
    viewed = models.IntegerField(editable=True, blank=True, null=True)

    def __str__(self):
        return self.title + ', ' + self.author.username

    def get_absolute_url(self):
        return f'/{self.pk}/'

    @property
    def number_of_comments(self):
        return BlogCommentModel.objects.filter(blog=self).count()


class BlogCommentModel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False, editable=True)
    date_posted = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.author.username) + "'s comment for " + self.blog.title
