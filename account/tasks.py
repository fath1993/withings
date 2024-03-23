import time

import jdatetime
import requests
from django.contrib.auth.models import User

from custom_logs.models import custom_log
from withings.settings import CLIENT_ID, SECRET


def refresh_tokens():
    users = User.objects.all()
    for user in users:
        profile = user.user_profile
        try:
            auth_withings_refresh_token_view(profile)
        except Exception as e:
            custom_log(f'{e}')
        time.sleep(1)


def auth_withings_refresh_token_view(profile):
    refresh_token_url = 'https://wbsapi.withings.net/v2/oauth2'

    payload = {
        'action': 'requesttoken',
        'grant_type': 'refresh_token',
        'client_id': f'{CLIENT_ID}',
        'client_secret': f'{SECRET}',
        'refresh_token': f'{profile.refresh_token}'
    }

    r = requests.post(refresh_token_url, data=payload)
    result_data = r.json()

    access_token = result_data['body']['access_token']
    refresh_token = result_data['body']['refresh_token']
    expires_in = result_data['body']['expires_in']

    profile.access_token = access_token
    profile.refresh_token = refresh_token
    profile.expiration_date = jdatetime.datetime.now() + jdatetime.timedelta(seconds=int(expires_in))
    profile.save()
