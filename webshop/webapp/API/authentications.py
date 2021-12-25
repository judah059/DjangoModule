from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from django.conf import settings
from rest_framework import exceptions


class TokenDeadAuthentication(TokenAuthentication):
    def authenticate(self, request):
        user, token = super(TokenDeadAuthentication, self).authenticate(request)
        delta = (timezone.now() - token.created).minutes
        if delta > settings.TOKEN_TIME_TO_LIVE:
            token.delete()
            msg = 'Invalid token. Time for token is over.'
            raise exceptions.AuthenticationFailed(msg)
        return user, token

    def perform_authentication(self, request):
        pass