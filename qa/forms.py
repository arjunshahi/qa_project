from django import forms

from qa.models import *


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'question']
class PostAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['ans']