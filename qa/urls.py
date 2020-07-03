from django.urls import path

from qa import views

app_name = 'qa'
urlpatterns = [
    path('home/', views.ListQuestions.as_view(), name='list_questions'),
    path('qa/<int:pk>/detail/', views.DetailQuestion.as_view(), name='question_detail'),
    path('create/qa/', views.CreateQuestion.as_view(), name='create_question'),
]
