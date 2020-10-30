from mptt.admin import MPTTModelAdmin

from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('id', 'author', 'published', 'active', 'deleted', 'content_type', 'object_id',)
    list_editable = ('active', 'deleted',)
