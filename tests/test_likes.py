import pytest

from likes import views

pytestmark = pytest.mark.django_db

class TestViews:
    def test_like_dislike(self, rf, create_like, create_user):
        url = '/thing/1/skirt/?dislike=1'
        user = create_user(email='user@email.com', email_confirm=True)
        like = create_like(user=user)
        req = rf.get(url)
        req.user = user
        req.META['HTTP_REFERER'] = '/thing/1/skirt/'
        resp = views.like_dislike(req)
        assert resp.status_code == 302

    def test_like_like(self, rf, create_like, create_user):
        url = '/thing/1/skirt/?like=1'
        user = create_user(email='user@email.com', email_confirm=True)
        like = create_like(user=user)
        req = rf.get(url)
        req.user = user
        req.META['HTTP_REFERER'] = '/thing/1/skirt/'
        resp = views.like_dislike(req)
        assert resp.status_code == 302

    def test_like_like_remove(self, rf, create_like, create_user):
        url = '/thing/1/skirt/?like_remove=1'
        user = create_user(email='user@email.com', email_confirm=True)
        like = create_like(user=user)
        req = rf.get(url)
        req.user = user
        req.META['HTTP_REFERER'] = '/thing/1/skirt/'
        resp = views.like_dislike(req)
        assert resp.status_code == 302

