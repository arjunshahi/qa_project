from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from users.forms import UserRegisterForm, UserLoginForm
from users.models import CustomUser, Profile


def login_user(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect('qa:list_questions')

            else:
                messages.error(request, 'Invalid Login Credentials.')
    return render(request, 'users/login.html', {'form': form})


def register_user(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            Profile.objects.create(user=user)
            print('///')
            # sending activation link to email here

            mail_subject = 'Please Activate Your Account'
            message = render_to_string('users/email_activation_template.html', {
                'user': user,
                'user_id': urlsafe_base64_encode(force_bytes(user.pk)),
                'domain': get_current_site(request).domain,
                'token': default_token_generator.make_token(user)
            })
            email = EmailMultiAlternatives(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.attach_alternative(message, 'text/html')
            email.send()
            messages.success(request, 'Your account has been created successfully.'
                                      'Please check your email to activate your account.')
            return redirect('users:register_user')
    return render(request, 'users/register.html', {'form': form})


def activate_user(request, user_id, token):
    try:
        pk = force_text(urlsafe_base64_decode(user_id))
        user = get_object_or_404(CustomUser, pk=pk)
    except Exception:
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully.'
                                  'Please login in order to access the homepage.')
        return redirect('/')
    else:
        return HttpResponse('Invalid Link')


def user_profile(request):
    return render(request, 'users/user_profile.html')
