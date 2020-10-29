from django.db import models
from django.db.models import Sum


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0).count()

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0).count()

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__published')