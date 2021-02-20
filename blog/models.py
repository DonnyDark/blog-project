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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.id}/'
