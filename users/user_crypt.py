from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.urls import reverse

CONFIRM_EMAIL_LIFETIME = 1


User = get_user_model()
signer = TimestampSigner(sep='/', salt='abrahadabra')


# create encode url with uuid
def encoder(scheme, host, user):
    # encode a uuid
    user_crypt = urlsafe_base64_encode(force_bytes(user.id))
    # sign encoded uuid
    signed_user = signer.sign(user_crypt)
    kwargs = {
        "signed_user": signed_user
    }
    # create activation url
    activation_url = reverse("users:activate_user_account", kwargs=kwargs)
    activate_url = "{0}://{1}{2}".format(scheme, host, activation_url)

    context = {
        'user': user,
        'activate_url': activate_url
    }
    return(context)


# decode url with userid
def decoder(request, signed_user):
    try:
        #check a signature
        user_encrypt = signer.unsign(signed_user, max_age=timedelta(days=CONFIRM_EMAIL_LIFETIME))
        signature = True
    except SignatureExpired:
        user_encrypt = signer.unsign(signed_user, max_age=timedelta(days=365))
        signature = False
    except (BadSignature):
        return None, None

    try:
        # decode user uuid
        uid = force_text(urlsafe_base64_decode(user_encrypt))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    return user, signature