from django import forms
from .models import Post, Comment


class AddCommentForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email',
        'class': 'form-control',
        'placeholder': 'Adresse e-mail'
    }))
    title = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'title',
        'class': 'form-control',
        'placeholder': 'Titre',
    }))
    body = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'body',
        'class': 'form-control',
        'rows': 8,
        'placeholder': 'Commentaire',
    }))

    class Meta:
        model = Comment
        fields = ['title', 'body', 'email']


class CommentUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email',
        'class': 'form-control',
        'placeholder': 'Adresse e-mail'
    }))
    title = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'title',
        'class': 'form-control',
        'placeholder': 'Titre',
    }))
    body = forms.CharField(widget=forms.Textarea(attrs={
        'id': 'body',
        'class': 'form-control',
        'rows': 8,
        'placeholder': 'Commentaire',
    }))
    class Meta:
        model = Comment
        fields = ['title', 'body', 'email']