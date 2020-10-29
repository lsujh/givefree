from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from .managers import LikeDislikeManager


User = get_user_model()

class LikeDislike(models.Model):
    vote = models.SmallIntegerField(verbose_name='Голос')
    user = models.ForeignKey(User, verbose_name='Користувач', related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikeDislikeManager()
