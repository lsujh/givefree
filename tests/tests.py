import pytest
import uuid

from django.contrib.auth import get_user_model
from django.urls import reverse
from django import urls
from django.utils import timezone

from users.models import TemporaryBanIp
from users.views import PasswordReset

User = get_user_model()


@pytest.fixture
def test_password():
    return 'password'

@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        kwargs['id'] = str(uuid.uuid4())
        kwargs['email_confirm'] = True
        kwargs['first_name'] = 'first_name'
        kwargs['last_name'] = 'last_name'
        return django_user_model.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user(email='super@test.com')
        client.login(email=user.email, password=test_password)
        return client, user
    return make_auto_login

@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('user@test.com', 'password')
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_auth_view(create_user, auto_login_user):
    user = create_user(email='super@test.com')
    client, user = auto_login_user(user)
    url = reverse('users:login')
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_user_detail(create_user, auto_login_user):
    user = create_user(email='user@test.com')
    client, user = auto_login_user(user)
    url = reverse('users:profile')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Профіль'.encode() in response.content

@pytest.mark.django_db
def test_superuser_detail(client, create_user):
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

@pytest.mark.django_db
def test_user_signup(client, create_user):
    assert User.objects.count() == 0
    signup_url = urls.reverse('users:signup')
    user = create_user(email='user_new@test.com')
    resp = client.post(signup_url)
    assert User.objects.count() == 1
    assert resp.status_code == 200

@pytest.mark.django_db
def test_user_login(client):
    login_url = urls.reverse('users:login')
    resp = client.post(login_url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_user_logout(create_user, auto_login_user):
    user = create_user(email='super@test.com')
    client, user = auto_login_user(user)
    logout_url = urls.reverse('users:logout')
    resp = client.get(logout_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse('freestuff:things_list')

@pytest.mark.django_db
def test_full_name(create_user):
    user = create_user(email='super@test.com')
    assert user.full_name() == 'first_name last_name'

@pytest.mark.django_db
def test_user_str(create_user):
    user = create_user(email='super@test.com')
    assert user.__str__() == 'super@test.com'

@pytest.mark.django_db
def test_ip_str():
    ip = TemporaryBanIp.objects.create(ip_address='0.0.0.0', time_unblock=timezone.now())
    assert ip.__str__() == '0.0.0.0'

# @pytest.mark.django_db
# def test_password_reset(create_user):
#     user = create_user(email='reset@test.com')

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