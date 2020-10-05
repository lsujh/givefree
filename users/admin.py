from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Profile

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'email', 'is_active', 'email_confirm']
    list_editable = ['email_confirm']
    list_filter = ('email', 'is_staff', 'is_active',)
    list_display_links = ('email',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('phone', 'street', 'postal_code', 'city')