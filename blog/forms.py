from django import forms
from .models import BlogModel, BlogCommentModel


class BlogCreationForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Please add a title. Max: 50 characters'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Max: 500 characters. Example: #name #Value #key and value'})
        }


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Starting typing your comment...'})
        }
