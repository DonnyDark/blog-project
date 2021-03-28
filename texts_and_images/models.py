from django.db import models

from blog.models import BlogModel


class TextOrImage(models.Model):
    blog = models.ForeignKey(BlogModel, related_name='text_or_image', on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return str(self.blog) + "'s object"