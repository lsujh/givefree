import pytest
from mixer.backend.django import mixer

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from users import views

User = get_user_model()
pytestmark = pytest.mark.django_db

class TestProfileView:
    def test_profile(self):
        User.objects.create_user('user@test.com', 'password')
        req = RequestFactory().get('profile/')
        req.session = {}
        req.user = mixer.blend(User)
        resp = views.profile(req)
        assert resp.status_code == 200

class TestLoginRequiredView:
    def test_anonymous(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        req.session = {}
        resp = views.CustomLoginView.as_view()(req)
        assert resp.status_code == 200

    def test_logged_in(self):
        User.objects.create_user('user@test.com', 'password')
        req = RequestFactory().get('/')
        req.session = {}
        req.user = mixer.blend(User)
        resp = views.CustomLoginView.as_view()(req)
        assert resp.status_code == 200