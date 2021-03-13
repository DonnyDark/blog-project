from django.contrib import admin
from .models import BlogModel, BlogCommentModel


admin.site.register(BlogModel)
admin.site.register(BlogCommentModel)
