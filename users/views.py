from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.contrib import messages
from django.views.generic import ListView

from .tasks import mail_send
from .user_crypt import decoder
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm, UserForm
from orders.models import Order


User = get_user_model()

class PasswordReset(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email__iexact = email).exists():
            messages.error(self.request, f"User with email {email} doesn\'t exists.")
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
            messages.success(request, 'Your profile was successfully updated!')
            return render(request, 'profile.html', {'user_form': user_form,
                                                    'profile_form': profile_form})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form,
                                                     'profile_form': profile_form})


class HistoryOrdersView(ListView):
    model = Order
    template_name = 'history_orders.html'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user.id)
        return queryset

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        auth_login(self.request, form.get_user(), backend='users.authenticate.CustomModelBackend')
        return HttpResponseRedirect(self.get_success_url())


