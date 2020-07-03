from django.urls import path

from users import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('activate/<user_id>/<token>/', views.activate_user, name='activate_user'),
    path('profile/', views.user_profile, name='user_profile'),
]
