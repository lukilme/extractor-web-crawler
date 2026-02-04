
from django import forms
from .models import Comment, NewsPost


class CommentForm(forms.ModelForm):
    """Formulário para comentários"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escreva seu comentário...'
            })
        }


class NewsPostForm(forms.ModelForm):
    
    class Meta:
        model = NewsPost
        fields = [
            'title',
            'summary',
            'content',
            'image',
            'source_url',
            'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'source_url': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }