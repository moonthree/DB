from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('article', 'user',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #fields = ('article', 'content',)
        exclude = ('article', 'user')
