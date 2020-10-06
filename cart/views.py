from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from freestuff.models import Things
from .cart import Cart
from .forms import CartAddThingForm
from coupons.forms import CouponApplyForm
from freestuff.recommender import Recommender


@require_POST
def cart_add(request, thing_pk):
    if '_delete' in request.POST:
        return cart_remove(request, thing_pk)
    request.session.pop('form_error', None)
    cart = Cart(request)
    thing = get_object_or_404(Things, pk=thing_pk)
    form = CartAddThingForm(request.POST)
    form.thing = thing
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(request, thing=thing, quantity=cd['quantity'], update_quantity=cd['update'], price=str(cd['price']))
    else:
        request.session['pk'] = thing.pk
        request.session['form_error'] = (thing.pk, form.errors['quantity'][0])
        request.session['slug'] = thing.slug

    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, thing_pk):
    cart = Cart(request)
    thing = get_object_or_404(Things, pk=thing_pk)
    cart.remove(thing)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    if not cart:
        if request.session.get('form_error'):
            return redirect('freestuff:thing_detail', pk=request.session['pk'], slug=request.session['slug'])
        return redirect('freestuff:things_list')
    for item in cart:
        item['update_quantity_form'] = CartAddThingForm(
            initial={'quantity': item['quantity'], 'update': True, 'price': item['price'],})
        if not item['thing_price']:
            item['update_quantity_form'].fields['price'].widget.attrs['readonly'] = False
            item['update_quantity_form'].fields['price'].__dict__['help_text'] = 'Введіть ціну, яку Ви готові заплатити'
    coupon_apply_form = CouponApplyForm()
    if cart:
        r = Recommender()
        cart_things = [item['thing'] for item in cart]
        recommender_things = r.suggest_things_for(cart_things, max_results=4)
    recommender_things = []
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form,
                                                'recommender_things': recommender_things})
