from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from qa.forms import *
from qa.models import *
from users.models import Profile


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
        """checking if the current user has voted on the question or not"""
        q_voted = question.question_votes.filter(user=request.user, question=question).exists()
        """getting the list of answers which are voted by the current user"""
        answers = Answer.objects.filter(question=question).annotate(answer_vote=Count('answer_votes')).\
            order_by('-is_accepted', '-answer_vote')
        a_voted_list = [answer for answer in answers if answer.answer_votes.filter(user=request.user, answer=answer)]
        context = {
            'question': question,
            'voted': q_voted,
            'a_voted_list': a_voted_list,
            'answers': answers
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
        if not question.user == request.user:
            QuestionVote.objects.get_or_create(question=question, user=request.user)
            vote_count = question.question_votes.count()
            # updating score of user
            Profile.objects.filter(user=question.user).update(score=F('score') + 10)
            data = {
                'msg': 'Voted',
                'count': vote_count,
                'score': question.user.profile.score,
            }
        else:
            data = {
                'msg': "Sorry.You can't vote your own post."
            }

        return JsonResponse(data)


class VoteAnswerView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        answer = get_object_or_404(Answer, pk=kwargs['pk'])
        if not answer.user == request.user:
            AnswerVote.objects.get_or_create(answer=answer, user=request.user)
            # updating score of user
            Profile.objects.filter(user=answer.user).update(score=F('score') + 10)
            data = {
                'msg': 'Voted',
                'count': answer.answer_votes.count(),
                'score': answer.user.profile.score,
            }
        else:
            data = {
                'msg': "Sorry. You can't vote your own post."
            }
        return JsonResponse(data)


class AcceptAnswerView(LoginRequiredMixin, View):
    def post(self, requst, **kwargs):
        answer = get_object_or_404(Answer, pk=kwargs['pk'])
        if not answer.is_accepted and answer.question.user == requst.user and not answer.user == requst.user:
            answer.is_accepted = True
            answer.save()
            """ updating score of user """
            Profile.objects.filter(user=answer.user).update(score=F('score') + 15)
            """
             filtering accepted answers of this question if it has any
            """
            ques_ans = answer.question.answers.all()
            accepted_ans = ques_ans.filter(is_accepted=True).exclude(pk=answer.pk)
            for answer in accepted_ans:
                answer.is_accepted = False
                answer.save()
            data = {
                'msg': 'Accepted.',
                'score': answer.user.profile.score
            }
        else:
            data = {
                'msg': 'Sorry.You can not accept your own answer.',
                'score': answer.user.profile.score
            }

        return JsonResponse(data)
