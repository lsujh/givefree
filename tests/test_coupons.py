import pytest
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from coupons import views

pytestmark = pytest.mark.django_db

class TestViews:
    def test_coupon_apply(self, rf):
        coupon = {'id':1, 'code':'123456789', 'valid_from':timezone.now() - timedelta(days=1),
                  'valid_to':timezone.now() + timedelta(days=1), 'activate':True}
        url = reverse('cart:cart_detail')
        req = rf.post(url, coupon)
        req.session = {}
        resp = views.coupon_apply(req)
        assert resp.status_code == 302

    def test_str(self, create_coupon):
        coupon = create_coupon(code='123456789')
        assert coupon.__str__() == '123456789'

