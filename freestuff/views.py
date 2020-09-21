from django.shortcuts import render, get_object_or_404
from .models import Category, Things
from cart.forms import CartAddThingForm
from .recommender import Recommender


def things_list(request, category_slug=None, category_pk=None):
    category = None
    categories = Category.objects.all()
    things = Things.objects.filter(is_active=True, quantity__gt=0)
    count = things.count()
    if category_slug and category_pk:
        category = get_object_or_404(
            Category, pk=category_pk).get_descendants(include_self=True)
        things = things.filter(category__in=category)
    return render(request, 'freestuff/list.html',
                  {'category': category,
                   'nodes': categories,
                   'things': things,
                   'count': count
                   })


def thing_detail(request, pk, slug):
    thing = get_object_or_404(Things, pk=pk, slug=slug)
    cart_thing_form = CartAddThingForm()
    r = Recommender()
    recommended_things = r.suggest_things_for([thing], 4)
    return render(request, 'freestuff/detail.html',
                  {'thing': thing,
                   'cart_thing_form': cart_thing_form,
                   'recommended_things': recommended_things
                   })
