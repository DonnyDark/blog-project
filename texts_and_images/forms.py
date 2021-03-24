from django import forms

from .models import TextOrImage


class TextCreationForm(forms.ModelForm):
    class Meta:
        model = TextOrImage
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10, 'placeholder': 'Starting typing your article...'}),
        }


class ImageCreationForm(forms.ModelForm):
    class Meta:
        model = TextOrImage
        fields = ['image']