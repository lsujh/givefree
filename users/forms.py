from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, \
    AuthenticationForm
from django.utils.text import capfirst

from .models import Profile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={
                            'placeholder': 'Введіть email'}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs=
                            {'autocomplete': 'new-password',
                            'placeholder': 'Введіть пароль'}), strip=False)
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs=
                            {'autocomplete': 'new-password',
                            'placeholder': 'Повторіть пароль'}), strip=False)
    use_required_attribute = False
    class Meta(UserCreationForm):
        model = User
        fields = ('email', )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'first_name', 'last_name', 'image')


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login':
            "Будь ласка введіть правильну електронну адресу та пароль.",
        'inactive': "Цей акаунт не активований.",}

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'street', 'postal_code', 'city', 'region', 'province')





