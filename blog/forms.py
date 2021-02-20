from django.forms import ModelForm
from .models import BlogModel, BlogCommentModel
from django import forms


class BlogCreationForm(ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Please add a title. Max: 50 characters'}),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 40, 'placeholder': 'Starting typing your article...'})
        }


class CommentCreationForm(ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 40, 'placeholder': 'Starting typing your comment...'})
        }