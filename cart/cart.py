from decimal import Decimal
from django.conf import settings
from django.db.models import F

from freestuff.models import Things
from coupons.models import Coupon


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            if self.session.get('coupon_id'):
                del self.session['coupon_id']
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        thing_ids = self.cart.keys()
        things = Things.objects.filter(id__in=thing_ids)
        cart = self.cart.copy()
        for thing in things:
            cart[str(thing.id)]['pk'] = thing.id
            cart[str(thing.id)]['thing'] = thing
            cart[str(thing.id)]['thing_price'] = thing.price
            cart[str(thing.id)]['thing_quantity'] = thing.quantity

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, request, thing, price, quantity=1, update_quantity=False):
        thing_id = str(thing.pk)
        if thing_id not in self.cart:
            self.cart[thing_id] = {'quantity': 0, 'price': str(0)}
        if update_quantity:
            self.cart[thing_id]['quantity'] = quantity
            self.cart[thing_id]['price'] = price
        else:
            self.cart[thing_id]['quantity'] = self.cart[thing_id]['quantity'] + (quantity
                if self.cart[thing_id]['quantity'] < thing.quantity else 0)
            self.cart[thing_id]['price'] = price

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, thing):
        thing_id = str(thing.id)
        if thing_id in self.cart:
            del self.cart[thing_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None