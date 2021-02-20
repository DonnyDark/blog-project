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
    published_date = models.DateField(default=timezone.now)

    liked = models.IntegerField(editable=True, blank=True, null=True)
    commented = models.IntegerField(editable=True, blank=True, null=True)
    viewed = models.IntegerField(editable=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog.views.blog_detail', args=[str(self.id)])


class BlogCommentModel(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False, editable=True)
