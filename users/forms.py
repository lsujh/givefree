from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.utils.text import capfirst

from .models import Profile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={
                            'placeholder': 'Введіль email'}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs=
                            {'autocomplete': 'new-password',
                            'placeholder': 'Введіть пароль'}), strip=False)
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs=
                            {'autocomplete': 'new-password',
                            'placeholder': 'Повторіть пароль'}), strip=False)
    use_required_attribute = False
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('email', )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'image')


class CustomAuthenticationForm(forms.Form):
    username = UsernameField(required=False, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        required=False,
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    error_messages = {
        'invalid_login':
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ,
        'inactive': "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = get_user_model()._meta.get_field(get_user_model().USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields['username'].max_length = username_max_length
        self.fields['username'].widget.attrs['maxlength'] = username_max_length
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login or password',
            )

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'address', 'postal_code', 'city')





