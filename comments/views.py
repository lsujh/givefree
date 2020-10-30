from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType

from badwordfilter.views import PymorphyProc, RegexpProc
from .forms import CommentForm
from .models import Comment


def add_comment(request, obj, comments):
    form = CommentForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        obj_type = ContentType.objects.get_for_model(obj)
        try:
            parent = comments.get(id=cd['parent'])
        except:
            parent = None
        content = PymorphyProc.replace(cd['content'], repl='***')
        content = RegexpProc.replace(content, repl='***')
        Comment.objects.create(
            content_type=obj_type, object_id=obj.id, author=cd['author'], parent=parent,
            email=cd['email'], content=content)
        return redirect(obj.get_absolute_url())


