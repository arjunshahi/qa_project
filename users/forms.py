from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(initial=True, required=False)


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
