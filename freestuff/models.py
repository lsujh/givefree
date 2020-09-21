from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.urls import reverse


class Category(MPTTModel):
    parent = TreeForeignKey('self', verbose_name='Батьківська категорія', related_name='children',
                               blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField('Назва', db_index=True, max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)

    class MPTTMeta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        #ordering = ('name',)
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('freestuff:things_list_by_category', args=[self.pk, self.slug])

    @property
    def items_count(self):
        ids = self.get_descendants(include_self=True).values_list('id')
        return Things.objects.filter(category_id__in=ids).count()


class Things(models.Model):
    category = TreeForeignKey(
        'Category', related_name='things', on_delete=models.CASCADE)
    name = models.CharField('Назва', max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)
    description = models.TextField('Опис', blank=True)
    size = models.PositiveIntegerField('Розмір', blank=True, null=True)
    image = models.ImageField('Фото', upload_to='things/%Y/%m/%d', blank=True)
    quantity = models.PositiveIntegerField('Кількість', default=1)
    is_active=models.BooleanField('Показати/сховати', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Річ'
        verbose_name_plural = 'Речі'
        ordering = ('name',)
        index_together = (('id', 'name'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('freestuff:thing_detail', args=[self.pk, self.slug])

