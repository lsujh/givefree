from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'email', 'content',)

    parent = forms.CharField(required=False, widget=forms.HiddenInput())