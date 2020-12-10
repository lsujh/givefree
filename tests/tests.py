import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from django import urls
from django.utils import timezone

from users.models import TemporaryBanIp


User = get_user_model()

@pytest.mark.asyncio
async def test_user_create(create_user):
    user = await create_user(email='super@test.com')
    assert user.objects.count() == 1


# @pytest.mark.django_db
# def test_user_create():
#     User.objects.create_user('user@test.com', 'password')
#     assert User.objects.count() == 1

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