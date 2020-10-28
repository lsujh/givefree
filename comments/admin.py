from mptt.admin import MPTTModelAdmin

from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('id', 'author', 'thing', 'published', 'active', 'deleted',)
    list_editable = ('active', 'deleted',)
