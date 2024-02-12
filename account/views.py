import requests
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse
from django.shortcuts import render, redirect

from utilities.http_metod import fetch_data_from_http_post
from withings.settings import CLIENT_ID, SECRET, OAUTH2_CALLBACK_URL
from custom_logs.models import custom_log
from requests_oauthlib import OAuth2Session


def auth_withings_view(request):
    AUTHORIZATION_URL = 'https://account.withings.com/oauth2_user/authorize2'
    withings = OAuth2Session(
        client_id=CLIENT_ID,
        redirect_uri=OAUTH2_CALLBACK_URL,
        scope="user.info,user.metrics,user.activity"
    )
    authorization_url, state = withings.authorization_url(AUTHORIZATION_URL)
    request.session['oauth_state'] = state
    return redirect(authorization_url)


def auth_withings_callback_view(request):
    TOKEN_URL = 'https://wbsapi.withings.net/v2/oauth2'

    payload = {
        'action': 'requesttoken',
        'grant_type': 'authorization_code',
        'client_id': f'{CLIENT_ID}',
        'client_secret': f'{SECRET}',
        'code': request.GET.get("code"),
        'redirect_uri': f'{OAUTH2_CALLBACK_URL}'
    }

    response = requests.post(TOKEN_URL, data=payload)
    token_data = response.json()

    # Store the token and other relevant information in your database
    custom_log(f'Token: {token_data}')
    custom_log(f'UserID: {token_data.get("userid")}')  # Assuming userid is included in the response

    return JsonResponse({"message": "Token obtained successfully"})


def login_view(request):
    context = {}
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'account/login.html', context)
        else:
            username = fetch_data_from_http_post(request, 'username', context)
            password = fetch_data_from_http_post(request, 'password', context)

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('website:index')
            else:
                context['err'] = 'کاربر با حساب فوق وجود ندارد'
                return render(request, 'account/login.html', context)
    else:
        return redirect('website:index')


def logout_view(request):
    logout(request)
    return redirect('website:index')



