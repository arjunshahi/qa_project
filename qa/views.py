from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from qa.forms import CreateQuestionForm
from qa.models import Question, QuestionViews


class ListQuestions(generic.ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'index.html'
    ordering = '-created'


class DetailQuestion(generic.DetailView):
    model = Question
    template_name = 'qa/post_detail.html'
    context_object_name = 'question'


class CreateQuestion(SuccessMessageMixin, generic.CreateView):
    model = Question
    template_name = 'base.html'
    form_class = CreateQuestionForm
    success_message = 'Your Question Posted Successfully.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('qa:question_detail', kwargs={'pk': self.object.pk})



