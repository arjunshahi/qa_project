from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.utils import timezone

from users.models import CustomUser

User = get_user_model()


class CommonInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(CommonInfo):
    title = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='title', unique_with='id')

    def __str__(self):
        return self.title


class Question(CommonInfo):
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_questions', null=True)


class QuestionVote(CommonInfo):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_votes')
    vote = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_votes_ques')


class QuestionViews(CommonInfo):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    session_key = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()


class Answer(CommonInfo):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    ans = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_answers')


class AnswerVote(CommonInfo):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_votes')
    vote = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes_ans')

