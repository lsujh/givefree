from taggit.models import Tag

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count, Sum, Prefetch
from django.utils import timezone

from .models import Post, Category, PostStatistic
from comments.forms import CommentForm
from comments.views import add_comment
from comments.models import Comment
from .forms import EmailPostForm
from likes.views import like_dislike
from bookmark.views import bookmark


def post_list(request, category_slug=None, tag_slug=None):
    object_list = Post.published.all()
    category = None
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    breadcrumb = category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug).get_descendants(
            include_self=True
        )
        object_list = object_list.filter(category__in=category)
        breadcrumb = category[0].get_ancestors(include_self=True)
    sort = request.GET.getlist("sort")
    object_list = object_list.order_by(*sort)
    paginator = Paginator(object_list, 3)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        "blog/post/list.html",
        {
            "page": page,
            "posts": posts,
            "category": category,
            "breadcrumb": breadcrumb,
            "tag": tag,
        },
    )


def post_detail(request, year, month, day, post):
    if request.GET:
        like_dislike(request)
    bookmark(request)
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    obj, created = PostStatistic.objects.get_or_create(
        date=timezone.now(), post=post, defaults={"post": post, "date": timezone.now()}
    )
    obj.views += 1
    obj.save(update_fields=["views"])
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        add_comment(request, post, comments)
    data = {}
    if request.user.is_authenticated:
        data["email"] = request.user.email
        data["author"] = request.user.full_name()
    form = CommentForm(initial=data)

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd["name"], cd["email"], post.title
            )
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd["name"], cd["comments"]
            )
            send_mail(subject, message, "admin@myblog.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
