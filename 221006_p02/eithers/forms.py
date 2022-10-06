from django import forms
from .models import Question, Comment

class QuestionForm(forms.ModelForm):
    issue_a = forms.CharField(
        label='RedTeam',
        widget=forms.TextInput(
            attrs={
                'maxlength': 500,
            }
        )
    )
    issue_b = forms.CharField(
        label='BlueTeam',
        widget=forms.TextInput(
            attrs={
                'maxlength': 500,
            }
        )
    )
    class Meta:
        model = Question
        fields = ('__all__')

class CommentForm(forms.ModelForm):
    # pick = forms.BooleanField(
    #     widget=forms.Select(
    #         choices=[
    #             (True, 'RedTeam'),
    #             (False, 'BlueTEAM'),
    #         ]
    #     )
    # )
    class Meta:
        model = Comment
        exclude = ('question',)