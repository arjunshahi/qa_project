from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from qa.forms import *
from qa.models import *


class ListQuestionsView(generic.ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'index.html'
    ordering = '-created'
    paginate_by = 10


class DetailQuestionView(LoginRequiredMixin, View):
    template_name = 'qa/post_detail.html'

    def get(self, request, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        voted = question.question_votes.filter(user=request.user, question=question).exists()
        context = {
            'question':question,
            'voted':voted
        }
        return render(request, self.template_name, context)


class CreateQuestionView(SuccessMessageMixin, generic.CreateView):
    model = Question
    template_name = 'base.html'
    form_class = CreateQuestionForm
    success_message = 'Your Question Posted Successfully.'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('qa:question_detail', kwargs={'pk': self.object.pk})


class PostAnswerView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        form = PostAnswerForm(request.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.question = question
            ans.user = request.user
            ans.save()
            return redirect('qa:question_detail', question.pk)


class VoteQuestionView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['pk'])
        QuestionVote.objects.get_or_create(question=question, user=request.user)
        data = {
            'msg': 'Voted'
        }
        return JsonResponse(data)


class VoteAnswerView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        answer = get_object_or_404(Answer, pk=kwargs['pk'])
        AnswerVote.objects.get_or_create(answer=answer, user=request.user)
        data = {
            'msg': 'Voted'
        }
        return JsonResponse(data)
