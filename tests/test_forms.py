import pytest
from mixer.backend.django import mixer

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail

from users import forms


User = get_user_model()
pytestmark = pytest.mark.django_db

class TestPostForm:
    def test_blank_form(self):
        form = forms.ProfileForm(data={})
        assert form.is_valid() is True

    def test_form_user_profile(self):
        user = User.objects.create_user('user@test.com', 'password')
        user_form = forms.UserForm(data={'user': user})
        profile_form = forms.ProfileForm(data={'user': user, 'phone': '9999999999'})
        assert (user_form.is_valid() and profile_form.is_valid()) is True
        # assert me== 'Ваш профіль був успішно оновлений!'

    # def test_correct_form(self):
    #     person = mixer.blend('intro.Person')
    #     form = forms.CommentForm(
    #         data={'person': person.pk, 'text': 'Some comment text'}
    #     )
    #     assert form.is_valid() is True, 'filled in form should be valid'

@pytest.mark.django_db
def test_password_reset(client, mailoutbox, rf):
    mail.send_mail('subject', 'body', 'from@example.com', ['to@example.com'])
    reset_request_url = reverse('users:password_reset')
    data = {'form_data': {'email': 'email@user.com',} }
    response = client.post(reset_request_url, data)
    assert response.status_code == 200
    assert len(mailoutbox) == 1
    m = mailoutbox[0]
    assert m.subject == 'subject'
    assert m.body == 'body'
    assert m.from_email == 'from@example.com'
    assert list(m.to) == ['to@example.com']
