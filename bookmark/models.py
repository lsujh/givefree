from django.db import models
from django.contrib.auth import get_user_model

from comments.models import Comment
from blog.models import Post


User = get_user_model()

class BookmarkBase(models.Model):
    class Meta:
        abstract = True
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BookmarkPost(BookmarkBase):
    obj = models.ForeignKey(Post, verbose_name='Стаття', on_delete=models.CASCADE )


class BookmarkComment(BookmarkBase):
    obj = models.ForeignKey(Comment, verbose_name='Коментар', on_delete=models.CASCADE)



