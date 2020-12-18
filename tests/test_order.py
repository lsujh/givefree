import pytest

from django.urls import reverse
from unittest.mock import Mock, MagicMock

from orders import views, forms

pytestmark = pytest.mark.django_db

class TestViews:
    def test_order_create(self, create_user, create_order, rf, create_thing, create_category):
        user = create_user(email='user@email.com')
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        order = {'first_name':'Ivan', 'last_name':'Ivanov', 'email':'user@email.com',
                 'phone':9999999999, 'city':'Kiev', 'shipping':'Ukrposhta',
                 'status':'Created', 'user':user}
        url = reverse('orders:order_create')
        req = rf.post(url, order)
        req.session = MagicMock()
        req.user = user
        form = forms.OrderCreateForm(req.POST)
        assert form.is_valid()
        resp = views.order_create(req)
        print(resp.content.decode())
        assert resp.status_code == 200

    def test_order_detail(self, create_user, create_order, create_thing, create_category, client):
        user = create_user(email='user@email.com')
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        order = create_order(user=user)
        url = reverse('orders:order_detail', kwargs={'order_id':order.id})
        resp = client.get(url)
        assert resp.status_code == 200
        assert 'Ivan Ivanov'.encode() in resp.content


