from django.urls import path

from qa import views

app_name = 'qa'
urlpatterns = [
    path('home/', views.ListQuestionsView.as_view(), name='list_questions'),
    path('question/<int:pk>/detail/', views.DetailQuestionView.as_view(), name='question_detail'),
    path('post/question/', views.CreateQuestionView.as_view(), name='create_question'),
    path('post/<int:pk>/answer/', views.PostAnswerView.as_view(), name='post_ans'),
    path('vote/<int:pk>/question/', views.VoteQuestionView.as_view(), name='vote_ques'),
    path('vote/<int:pk>/answer/', views.VoteAnswerView.as_view(), name='vote_ans'),
    path('accept/<int:pk>/answer/', views.AcceptAnswerView.as_view(), name='accept_ans')
]
