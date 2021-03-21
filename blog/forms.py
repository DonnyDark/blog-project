from django import forms
from .models import BlogModel, BlogCommentModel


class BlogCreationForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'text', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Please add a title. Max: 50 characters'}),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder': 'Starting typing your article...'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Please add tags separated by commas. Max: 500 characters'})
        }


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': 'Starting typing your comment...'})
        }