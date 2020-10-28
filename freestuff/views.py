from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from .models import Category, Things
from cart.forms import CartAddThingForm
from .recommender import Recommender
from comments.forms import CommentForm


@require_GET
def robots_txt(request):
    lines = [
        'User-Agent: *',
        'Disallow: /admin/',
        'Disallow: /account/',
        'Disallow: /orders/',
        'Disallow: /coupons/',
        'Disallow: /cart/',
    ]
    return HttpResponse("\n".join(lines), content_type='text/plain')


def things_list(request, category_slug=None, category_pk=None):
    request.session['referer'] = request.build_absolute_uri()
    request.session.pop('form_error', None)
    category = None
    categories = Category.objects.all()
    things = Things.objects.filter(is_active=True, quantity__gt=0)
    count = things.count()
    breadcrumb = category
    if request.GET.get('q'):
        query = request.GET.get('q')
        things = Things.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) |
                                       Q(category__name__icontains=query))
        data = {'category': category,
                       'nodes': categories,
                       'things': things,
                       'count': count,
                       'breadcrumb': breadcrumb
                       }
    else:
        if category_slug and category_pk:
            category = get_object_or_404(Category, pk=category_pk).get_descendants(include_self=True)
            things = things.filter(category__in=category)
            breadcrumb = category[0].get_ancestors(include_self=True)
        data = {'category': category,
                       'nodes': categories,
                       'things': things,
                       'count': count,
                       'breadcrumb': breadcrumb
                       }
    paginator = Paginator(things, 12)
    page = request.GET.get('page')
    try:
        things = paginator.page(page)
    except PageNotAnInteger:
        things = paginator.page(1)
    except EmptyPage:
        things = paginator.page(paginator.num_pages)
    data.update({'page': page, 'things': things})
    return render(request, 'freestuff/list.html', data)


def thing_detail(request, pk, slug):
    context = {}
    request.session['referer'] = request.build_absolute_uri()
    context['thing'] = get_object_or_404(Things, pk=pk, slug=slug)
    context['meta'] = context['thing'].as_meta()
    context['cart_thing_form'] = CartAddThingForm(initial={'price': context['thing'].price})
    context['breadcrumb'] = context['thing'].category.get_ancestors(include_self=True)
    context['comments'] = context['thing'].comments.filter(active=True)
    if not context['thing'].price:
        context['cart_thing_form'].fields['price'].widget.attrs['readonly'] = False
        context['cart_thing_form'].fields['price'].__dict__['help_text'] = 'Введіть ціну, яку Ви готові заплатити'
    r = Recommender()
    context['recommended_things'] = r.suggest_things_for([context['thing']], 4)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            try:
                new_comment.parent = context['comments'].get(id=form.cleaned_data['parent'])
            except:
                pass
            new_comment.thing = context['thing']
            new_comment.save()
            return redirect(context['thing'].get_absolute_url())
    data = {}
    if request.user.is_authenticated:
        data['email'] = request.user.email
        data['author'] = request.user.full_name()
    context['form'] = CommentForm(initial=data)
    return render(request, 'freestuff/detail.html', context)


