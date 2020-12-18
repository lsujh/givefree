import pytest
from mixer.backend.django import mixer

from django.urls import  reverse
from django.core.signing import TimestampSigner
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage import default_storage

from django.utils import timezone

from users import user_crypt
from users.models import TemporaryBanIp
from users import views

User = get_user_model()
pytestmark = pytest.mark.django_db
signer = TimestampSigner(sep='/', salt='abrahadabra')

class TestUserCrypt:
    def test_encoder(self, create_user):
        user = create_user(email='user@email.com')
        context = user_crypt.encoder('http', 'localhost', user)
        assert user == context['user']

    def test_decoder(self, create_user, rf):
        user = create_user(email='user@email.com')
        crypt = urlsafe_base64_encode(force_bytes(user.id))
        signed_user = signer.sign(crypt)
        url = f'/account/activate/{signed_user}/'
        req = rf.get(url)
        user, signature = user_crypt.decoder(req, signed_user)
        assert signature
        assert user

    def test_decoder_not_user(self, rf):
        crypt = urlsafe_base64_encode(force_bytes('01f18dd7-c9da-4154-9d43-1b981c1c3742'))
        signed_user = signer.sign(crypt)
        url = f'/account/activate/{signed_user}/'
        req = rf.get(url)
        user, signature = user_crypt.decoder(req, signed_user)
        assert signature
        assert not user

    def test_decoder_badsignature(self, rf):
        signed_user = 'NjBiMzdlYxldygvKriRBYDi6G5hYk'
        url = f'/account/activate/NjBiMgvKriRBYDi6G5hYk/'
        req = rf.get(url)
        user, signature = user_crypt.decoder(req, signed_user)
        assert not signature
        assert not user

class TestUser:
    def test_user_create(self):
        User.objects.create_user('user@test.com', 'password')
        assert User.objects.count() == 1

    def test_auth_view(self, create_user, auto_login_user):
        user = create_user(email='super@test.com')
        client, user = auto_login_user(user)
        url = reverse('users:login')
        response = client.get(url)
        assert response.status_code == 302

    def test_user_detail(self, create_user, auto_login_user):
        user = create_user(email='user@test.com')
        client, user = auto_login_user(user)
        url = reverse('users:profile')
        response = client.get(url)
        assert response.status_code == 200
        assert 'Профіль'.encode() in response.content

    def test_superuser_detail(self, client, create_user):
        admin_user = create_user(email='super@test.com', is_staff=True, is_superuser=True)
        client.login(email='super@test.com', password='password')
        url = reverse('users:profile')
        response = client.get(url)
        assert response.status_code == 200
        assert 'Профіль'.encode() in response.content

    # @pytest.mark.django_db
    # def test_send_report(auto_login_user, mailoutbox):
    #    client, user = auto_login_user()
    #    url = reverse('send-report-url')
    #    response = client.post(url)
    #    assert response.status_code == 201
    #    assert len(mailoutbox) == 1
    #    mail = mailoutbox[0]
    #    assert mail.subject == f'Report to {user.email}'
    #    assert list(mail.to) == [user.email]

    def test_user_signup(self, client, create_user):
        assert User.objects.count() == 0
        signup_url = reverse('users:signup')
        user = create_user(email='user_new@test.com')
        resp = client.post(signup_url)
        assert User.objects.count() == 1
        assert resp.status_code == 200

    def test_user_login(self, client):
        login_url = reverse('users:login')
        resp = client.post(login_url)
        assert resp.status_code == 200

    def test_user_logout(self, create_user, auto_login_user):
        user = create_user(email='super@test.com')
        client, user = auto_login_user(user)
        logout_url = reverse('users:logout')
        resp = client.get(logout_url)
        assert resp.status_code == 302
        assert resp.url == reverse('freestuff:things_list')

    def test_full_name(self, create_user):
        user = create_user(email='super@test.com')
        assert user.full_name() == 'first_name last_name'

    def test_user_str(self, create_user):
        user = create_user(email='super@test.com')
        assert user.__str__() == 'super@test.com'

    def test_ip_str(self):
        ip = TemporaryBanIp.objects.create(ip_address='0.0.0.0', time_unblock=timezone.now())
        assert ip.__str__() == '0.0.0.0'

    def test_password_reset(self, client, create_user):
        user = create_user(email='reset@test.com')
        url = reverse('users:password_reset')
        resp = client.get(url, data={'email': 'email@email.com'})
        assert resp.status_code == 200
        assert 'Перевстановлення паролю'.encode() in resp.content

    # @pytest.mark.django_db
    # @pytest.mark.parametrize('param', [
    # 	('users:signup'),
    # ])
    # def test_render_views(client, param):
    #     temp_url = urls.reverse(param)
    #     resp = client.get(temp_url)
    #     assert resp.status_code == 200

    # @pytest.mark.django_db
    # @pytest.mark.parametrize('param', [
    # 	('users:profile'),
    # ])
    # def test_render_views(client, param):
    #     temp_url = urls.reverse(param)
    #     resp = client.get(temp_url)
    #     assert resp.status_code == 302

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

    def test_singup(self, client):
        url = reverse('users:signup')
        resp = client.post(url, data={'email': 'email@email.com', 'password1': '12password34',
                                                     'password2': '12password34'})
        assert resp.status_code == 200
        assert 'Ласкаво просимо!'.encode() in resp.content