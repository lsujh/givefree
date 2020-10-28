from mptt.models import MPTTModel, TreeForeignKey
from django.db import models

from freestuff.models import Things


class Comment(MPTTModel):
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    author = models.CharField(max_length=50, verbose_name='Автор')
    email = models.EmailField(verbose_name='Email')
    content = models.TextField(verbose_name='Повідомлення')
    published = models.DateTimeField(verbose_name='Дата публікації', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата оновлення', auto_now=True)
    thing = models.ForeignKey(Things, on_delete=models.CASCADE, related_name='comments')
    active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    class MPTTMeta:
        order_insertion_by = ['-published']

    def __str__(self):
        return f'{self.author} {self.thing}'

