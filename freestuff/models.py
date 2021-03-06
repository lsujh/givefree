from mptt.models import MPTTModel, TreeForeignKey
from easy_thumbnails.fields import ThumbnailerImageField
from meta.models import ModelMeta

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation

from comments.models import Comment
from givefree.fields import ListField


User = get_user_model()


class Category(MPTTModel):
    parent = TreeForeignKey(
        "self",
        verbose_name="Батьківська категорія",
        related_name="children",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField("Назва", db_index=True, max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)

    class MPTTMeta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("freestuff:things_list_by_category", args=[self.pk, self.slug])

    @property
    def items_count(self):
        ids = self.get_descendants(include_self=True).values_list("id")
        return Things.objects.filter(category_id__in=ids).count()


class Things(ModelMeta, models.Model):
    category = TreeForeignKey(
        "Category",
        related_name="things",
        on_delete=models.CASCADE,
        verbose_name="Категорія",
    )
    name = models.CharField(verbose_name="Назва", max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)
    description = models.TextField(verbose_name="Опис", blank=True)
    size = models.PositiveIntegerField(verbose_name="Розмір", blank=True, default=0)
    quantity = models.PositiveIntegerField(verbose_name="Кількість", default=1)
    is_active = models.BooleanField(verbose_name="Активний", default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(
        verbose_name="Ціна", max_digits=5, decimal_places=0, blank=True, default=0
    )
    keywords = ListField(verbose_name="Ключові слова")
    owner = models.ForeignKey(
        User, verbose_name="власник", on_delete=models.CASCADE, related_name="thing"
    )
    comments = GenericRelation(Comment, related_query_name="thing")

    class Meta:
        verbose_name = "Річ"
        verbose_name_plural = "Речі"
        ordering = ("name",)
        index_together = (("id", "name"),)

    # class MPTTMeta:
    #     order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("freestuff:thing_detail", args=[self.pk, self.slug])

    def save(self, *args, **kwargs):
        self.keywords.append(self.name.split()[0].lower())
        cat_name = (
            Category.objects.get(name=self.category.name)
            .get_ancestors(include_self=True)
            .values_list("name", flat=True)
        )
        for name in cat_name:
            self.keywords.append(name.lower())
        super(self.__class__, self).save(*args, **kwargs)

    _metadata = {
        "title": "name",
        "description": "description",
        "keywords": "keywords",
    }


class Images(ModelMeta, models.Model):
    thing = models.ForeignKey(Things, on_delete=models.CASCADE, related_name="images")
    main = models.BooleanField(verbose_name="Основна", default=False)
    image = ThumbnailerImageField(
        verbose_name="Фото",
        upload_to="things/%Y/%m/%d",
        resize_source=dict(quality=100, size=(1000, 1000), sharpen=True),
    )

    _metadata = {
        "image": "get_meta_image",
    }

    def get_meta_image(self):
        if self.image:
            return self.image.image
