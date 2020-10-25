# -*- coding: utf-8 -*-
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import get_language
from django.contrib import messages
from django.utils.http import is_safe_url, urlunquote
from django.contrib import auth
from django.views import View
from django.utils import timezone


from .tasks import mail_send
from .user_crypt import decoder
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm, UserForm
from .models import TemporaryBanIp

User = get_user_model()

class PasswordReset(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email__iexact = email).exists():
            messages.error(self.request, f"Користувач з таким email {email} не існує.")
            return render(self.request, 'registration/password_reset_form.html')
        return super().form_valid(form)

def activate_user_account(request, signed_user=None):
    user, signature = decoder(request, signed_user)
    if user and signature:
        user.email_confirm = True
        user.save()
        return render(request, 'email_verify_done.html', {'user': user})
    elif user:
        host = request.get_host()
        scheme = request.scheme
        lang = get_language()
        mail_send.delay(lang, scheme, host, user.id)
        return render(request, 'email_verify_end_of_time.html')
    else:
        return render(request, 'user_does_not_exist.html')


def signup(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            host = request.get_host()
            scheme = request.scheme
            mail_send.delay(scheme, host, new_user.id)
            return render(request, 'registration/signup_done.html', {'new_user': new_user})
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'user_form': user_form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профіль був успішно оновлений!')
            return render(request, 'profile.html', {'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    })
        else:
            messages.error(request, 'Будь-ласка виправте помилку нижче.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form,
                                                     'profile_form': profile_form})


class CustomLoginView(View):
    def get(self, request):
        if auth.get_user(request).is_authenticated:
            return redirect('/')
        else:
            form = CustomAuthenticationForm
            return render(request, 'registration/login.html', {'form': form})
    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        ip = get_client_ip(request)
        obj, created = TemporaryBanIp.objects.get_or_create(ip_address=ip,
            defaults={'ip_address': ip, 'time_unblock': timezone.now()})
        if obj.status is True and obj.time_unblock > timezone.now():
            if obj.attempts == 3 or obj.attempts == 6:
               return render(request, 'block_15_minutes.html')
            elif obj.attempts == 9:
                return render(request, 'block_24_hours.html')
        elif obj.status is True and obj.time_unblock < timezone.now():
            obj.status = False
            obj.save()

        if form.is_valid():
            auth.login(request, form.get_user(), backend='users.authenticate.CustomModelBackend')
            obj.delete()
            # next = urlparse(get_next_url(request)).path
            next = request.session.get('referer', '/')
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            return redirect(next)
        else:
            obj.attempts += 1
            if obj.attempts == 3 or obj.attempts == 6:
                obj.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
                obj.status = True
            elif obj.attempts == 9:
                obj.time_unblock = timezone.now() + timezone.timedelta(1)
                obj.status = True
            elif obj.attempts > 9:
                obj.attempts = 1
            obj.save()

        return render(request, 'registration/login.html', {'form': form})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def get_next_url(request):
#     next = request.META.get('HTTP_REFERER')
#     if next:
#         next = urlunquote(next)
#     if not is_safe_url(url=next, allowed_hosts=request.get_host()):
#         next = '/'
#     return next


