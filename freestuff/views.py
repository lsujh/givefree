from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

from .models import Category, Things
from cart.forms import CartAddThingForm
from .recommender import Recommender


def things_list(request, category_slug=None, category_pk=None):
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
    thing = get_object_or_404(Things, pk=pk, slug=slug)
    cart_thing_form = CartAddThingForm(initial={'price': thing.price})
    breadcrumb = thing.category.get_ancestors(include_self=True)
    if not thing.price:
        cart_thing_form.fields['price'].widget.attrs['readonly'] = False
    r = Recommender()
    recommended_things = r.suggest_things_for([thing], 4)
    return render(request, 'freestuff/detail.html',
                  {'thing': thing, 'breadcrumb': breadcrumb,
                   'cart_thing_form': cart_thing_form,
                   'recommended_things': recommended_things,
                   })


# class SearchResultsView(ListView):
#     model = Things
#     template_name = 'freestuff/search_results.html'
#     def get_queryset(self):
#         query = self.request.GET.get('q')
#         object_list = Things.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
#         return object_list
