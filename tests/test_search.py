import pytest

from django.urls import reverse

from search import views

pytestmark = pytest.mark.django_db

class TestViews:
    def test_Search_View(self, rf):
        url = reverse('search:index')
        req = rf.get(url, {'q': 'last'})
        req.session = {}
        resp = views.SearchView.as_view()(req)
        assert resp.status_code == 200


