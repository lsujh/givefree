import pytest

from django.urls import reverse

from freestuff import views

pytestmark = pytest.mark.django_db

class TestViews:
    def test_thing_list(self, rf, create_category, create_thing):
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        url = f"/things/{category.pk}/{category.slug}/"
        req = rf.get(url)
        req.session = {}
        resp = views.things_list(req)
        assert resp.status_code == 200
        assert 'Dress'.encode() in resp.content

    def test_thing_detail(self, rf, create_thing, create_category, client):
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        kwargs = {'pk':thing.pk, 'slug':thing.slug}
        url = reverse("freestuff:thing_detail", kwargs=kwargs)
        resp = client.get(url)
        assert resp.status_code == 200
        assert 'Skirt'.encode() in resp.content


