from django import forms

from qa.models import Question


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'question']
