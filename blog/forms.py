from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import BlogModel, BlogCommentModel


class BlogCreationForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Please add a title. Max: 50 characters'}),
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder': 'Starting typing your article...'})
        }

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': 'Starting typing your comment...'})
        }