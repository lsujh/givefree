from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from .models import LikeDislike
from comments.models import Comment

User = get_user_model()

def like_dislike(request):
    like = request.GET.get('like')
    dislike = request.GET.get('dislike')
    like_remove = request.GET.get('like_remove')
    if like:
        obj = Comment.objects.get(id=int(like))
        obj_type = ContentType.objects.get_for_model(obj)
        LikeDislike.objects.update_or_create(
            content_type=obj_type, object_id=obj.id, user=request.user, defaults={'vote': 1})

    elif dislike:
        obj = Comment.objects.get(id=int(dislike))
        obj_type = ContentType.objects.get_for_model(obj)
        LikeDislike.objects.update_or_create(
            content_type=obj_type, object_id=obj.id, user=request.user, defaults={'vote': -1})

    elif like_remove:
        obj = Comment.objects.get(id=int(like_remove))
        obj_type = ContentType.objects.get_for_model(obj)
        LikeDislike.objects.filter(
            content_type=obj_type, object_id=obj.id, user=request.user).delete()

    return redirect(request.META.get('HTTP_REFERER'))

