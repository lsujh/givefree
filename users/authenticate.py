from django.contrib.auth.backends import ModelBackend


class CustomModelBackend(ModelBackend):

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        can = super(CustomModelBackend, self).user_can_authenticate(user)

        if can:
            return user.email_confirm
        return can