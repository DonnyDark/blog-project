import uuid
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class BlogModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    text = models.TextField()

    '''
    published_date = models.DateField()
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'pk': self.pk})
    '''