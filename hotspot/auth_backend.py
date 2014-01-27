from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialToken


class OAuthTokenBackend(object):
    """Log in to Django using an oauth token

    """
    def authenticate(self, token=None):
        try:
            return SocialToken.objects.get(token=token).account.user
        except SocialToken.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
