import pytest

from django.urls import  reverse
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from users import user_crypt

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
        signed_user = 'NjBiMzdlYmEtMjRiMy00YWI4LTkwZDctZmM4MDYwM2ExNzk3/1kpuXd/U7hGoyo-EihUKApSkz5iEooxldygvKriRBYDi6G5hYk'
        url = f'/account/activate/NjBiMzdlYmEtMjRiMy00YWI4LTkwZDctZmM4MDYwM2ExNzk3/1kpuXd/U7hGoyo-EihUKApSkz5iEooxldygvKriRBYDi6G5hYk/'
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
