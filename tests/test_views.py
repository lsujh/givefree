import pytest
from mixer.backend.django import mixer

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.messages.storage import default_storage

from users import views

User = get_user_model()
pytestmark = pytest.mark.django_db

class TestProfileView:
    def test_profile(self, rf):
        User.objects.create_user('user@test.com', 'password')
        req = rf.get('profile/')
        req.session = {}
        req.user = mixer.blend(User)
        resp = views.profile(req)
        assert resp.status_code == 200

    def test_profile_post(self, rf, client):
        user = User.objects.create_user('user@test.com', 'password')
        client.force_login(user)
        req = rf.post('profile/', {})
        req.session = {}
        req.user = mixer.blend(User)
        req._messages = default_storage(req)
        resp = views.profile(req)
        assert resp.status_code == 200

class TestLoginRequiredView:
    def test_anonymous(self, rf):
        req = rf.get('/')
        req.user = AnonymousUser()
        req.session = {}
        resp = views.CustomLoginView.as_view()(req)
        assert resp.status_code == 200

    def test_logged_in(self, rf):
        User.objects.create_user('user@test.com', 'password')
        req = rf.get('/')
        req.session = {}
        req.user = mixer.blend(User)
        resp = views.CustomLoginView.as_view()(req)
        assert resp.status_code == 200

class TestSignupView:
    def test_signup(self, rf):
        req = rf.get('signup/')
        req.session = {}
        resp = views.signup(req)
        assert resp.status_code == 200
        assert 'Реєстрація'.encode() in resp.content

    def test_signup_post(self, rf):
        user = User.objects.create_user('user@test.com', 'password')
        req = rf.post('signup/', {})
        req.session = {}
        req.user = mixer.blend(User)
        resp = views.signup(req)
        assert resp.status_code == 200
        assert 'Ласкаво просимо!'.encode() in resp.content


