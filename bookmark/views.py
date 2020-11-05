import json

from django.contrib import auth
from .models import BookmarkPost


def bookmark(request):
    pk = request.GET.get('bookmark')
    user = auth.get_user(request)
    if user.is_authenticated and pk:
        bookmark, created = BookmarkPost.objects.get_or_create(user=user, obj_id=pk)
        if not created:
            bookmark.delete()


