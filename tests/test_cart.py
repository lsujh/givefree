import pytest

from django.urls import reverse

from cart import views


pytestmark = pytest.mark.django_db

class TestViews:
    def test_cart_add(self, client, rf, create_thing, create_category):
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        data = {'quantity': 1, 'price': 0}
        kwargs = {'thing_pk':thing.pk}
        url = reverse('cart:cart_add', kwargs=kwargs)
        resp = client.post(url, data)
        assert resp.status_code == 302

    def test_cart_remove(self, client, rf, create_thing, create_category):
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        kwargs = {'thing_pk':thing.pk}
        url = reverse('cart:cart_remove', kwargs=kwargs)
        resp = client.post(url)
        assert resp.status_code == 302

    def test_cart_detail(self, client, rf, create_category, create_thing):
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        url = reverse('cart:cart_detail')
        req = rf.get(url)
        req.session = {}
        req.session['modified'] = True
        req.session['cart'] = {'1':{'thing':thing, 'price':0, 'quantity':1}}
        resp = views.cart_detail(req)
        assert resp.status_code == 200

