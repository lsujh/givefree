import markdown

from django import template
from django.utils import timezone
from django.db.models import Count, Sum
from django.utils.safestring import mark_safe

from ..models import Post, PostStatistic, Category


register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("blog/post/category_posts.html")
def show_category_posts():
    categories = Category.objects.all()
    return {"categories": categories}


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.inclusion_tag("blog/post/popular_posts.html")
def show_popular_posts(count=5):
    popular_posts = (
        PostStatistic.objects.filter(
            date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]
        )
        .values("post__slug", "post__title", "post__publish")
        .annotate(views=Sum("views"))
        .order_by("-views")[:count]
    )
    for pop in popular_posts:
        pop["date"] = [
            int(i) for i in pop["post__publish"].strftime("%Y.%m.%d").split(".")
        ]
    return {"popular_posts": popular_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter
def user_in(objects, user):
    if user.is_authenticated:
        return objects.filter(user=user).exists()
    return False
