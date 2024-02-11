from base64 import b64encode

from django.contrib.auth.models import User

from accounts.models import Profile
from accounts.serializer import ProfileSerializer
from hashlib import sha1
import hmac

from django.conf import settings
from django.http.response import Http404
from django.utils import timezone

from utilities.utilities import get_client_ip
from custom_logs.models import custom_log


def verified_signature_required(function):
    def wrapper(request, *args, **kwargs):
        signature = request.META.get('HTTP_X_FITBIT_SIGNATURE')
        if signature:
            key = bytes(f'{settings.FITBIT_CLIENT_SECRET}&', 'utf-8')
            hashed = hmac.new(key, request.body, sha1)
            computed_signature = b64encode(hashed.digest())
            if computed_signature != signature.encode('utf-8'):
                ip_addr, _ = get_client_ip(request)
                custom_log(f'Suspicious "updates" notification from IP: %s {ip_addr}')
                raise Http404
        return function(request, *args, **kwargs)
    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


def add_subscription(fitbit_user: Profile):
    client = fitbit_user.client
    return client.subscription(fitbit_user.user.username, None)


def create_user_profile(credentials: dict):
    access_token = credentials.get('access_token')
    refresh_token = credentials.get('refresh_token')
    expires_at = timezone.now() + (
        timezone.timedelta(seconds=credentials.get('expires_in')))
    scope = credentials.get('scope')
    user_id = credentials.get('user_id')
    user, _ = User.objects.get_or_create(username=user_id)
    data = {
        'scope': scope,
        'refresh_token': refresh_token,
        'access_token': access_token,
        'expires_at': expires_at,
    }
    fitbit_user, created = Profile.objects.update_or_create(
        user=user, defaults=data)
    fitbit_user.refresh_profile()
    if created:
        add_subscription(fitbit_user)
    return fitbit_user
