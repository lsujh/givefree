from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from likes.models import LikeDislike


class Comment(MPTTModel):
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    author = models.CharField(max_length=50, verbose_name='Автор')
    email = models.EmailField(verbose_name='Email')
    content = models.TextField(verbose_name='Повідомлення')
    published = models.DateTimeField(verbose_name='Дата публікації', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата оновлення', auto_now=True)
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    likes = GenericRelation(LikeDislike, related_query_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    class MPTTMeta:
        order_insertion_by = ['-published']

    def __str__(self):
        return f'{self.author} {self.thing}'