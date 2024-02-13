import jdatetime
import requests
from django.contrib.auth import authenticate, logout, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from knox.auth import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from account.models import Profile
from account.serializer import ProfileSerializer
from utilities.http_metod import fetch_data_from_http_post
from utilities.utilities import create_json
from withings.settings import CLIENT_ID, SECRET, OAUTH2_CALLBACK_URL
from custom_logs.models import custom_log
from requests_oauthlib import OAuth2Session





def auth_withings_view(request):
    if request.user.is_authenticated:
        AUTHORIZATION_URL = 'https://account.withings.com/oauth2_user/authorize2'
        withings = OAuth2Session(
            client_id=CLIENT_ID,
            redirect_uri=OAUTH2_CALLBACK_URL,
            scope="user.info,user.metrics,user.activity"
        )
        authorization_url, state = withings.authorization_url(AUTHORIZATION_URL)
        request.session['oauth_state'] = state
        return redirect(authorization_url)
    else:
        return redirect('accounts:login')


def auth_withings_callback_view(request):
    if request.user.is_authenticated:
        TOKEN_URL = 'https://wbsapi.withings.net/v2/oauth2'

        payload = {
            'action': 'requesttoken',
            'grant_type': 'authorization_code',
            'client_id': f'{CLIENT_ID}',
            'client_secret': f'{SECRET}',
            'code': request.GET.get("code"),
            'redirect_uri': f'{OAUTH2_CALLBACK_URL}'
        }

        r = requests.post(TOKEN_URL, data=payload)
        result_data = r.json()

        profile = request.user.user_profile
        userid = result_data['body']['userid']
        access_token = result_data['body']['access_token']
        refresh_token = result_data['body']['refresh_token']
        scope = result_data['body']['scope']
        expires_in = result_data['body']['expires_in']
        token_type = result_data['body']['token_type']
        profile.userid = userid
        profile.access_token = access_token
        profile.refresh_token = refresh_token
        profile.scope = scope
        profile.expiration_date = jdatetime.datetime.now() + jdatetime.timedelta(seconds=int(expires_in))
        profile.token_type = token_type
        profile.save()
        custom_log(f'Data: {result_data}')

        return redirect('website:index')
    else:
        return redirect('accounts:login')


def auth_withings_refresh_token_view(request):
    if request.user.is_authenticated:
        refresh_token_url = 'https://wbsapi.withings.net/v2/oauth2'

        payload = {
            'action': 'requesttoken',
            'grant_type': 'refresh_token',
            'client_id': f'{CLIENT_ID}',
            'client_secret': f'{SECRET}',
            'refresh_token': f'{request.user.user_profile.refresh_token}'
        }

        r = requests.post(refresh_token_url, data=payload)
        result_data = r.json()
        profile = request.user.user_profile
        userid = result_data['body']['userid']
        access_token = result_data['body']['access_token']
        refresh_token = result_data['body']['refresh_token']
        scope = result_data['body']['scope']
        expires_in = result_data['body']['expires_in']
        token_type = result_data['body']['token_type']
        profile.userid = userid
        profile.access_token = access_token
        profile.refresh_token = refresh_token
        profile.scope = scope
        profile.expiration_date = jdatetime.datetime.now() + jdatetime.timedelta(seconds=int(expires_in))
        profile.token_type = token_type
        profile.save()
        custom_log(f'Data: {result_data}')

        return redirect('website:index')
    else:
        return redirect('accounts:login')


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
    if request.user.is_authenticated:
        logout(request)
    return redirect('accounts:login')


class Account(APIView):
    # authentication_classes = (TokenAuthentication,)
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'عملیات حساب کاربری'}

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user)
        if profile.count() == 0:
            return JsonResponse(
                create_json('post', 'جزئیات حساب کاربری', 'ناموفق', f'حساب کاربری یافت نشد'))
        serializer = ProfileSerializer(profile, many=True)
        result_data = serializer.data
        for data in result_data:
            data['email'] = request.user.email
        json_response_body = {
            'method': 'post',
            'request': 'جزئیات حساب کاربری',
            'result': 'موفق',
            'data': result_data,
        }
        return JsonResponse(json_response_body)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user)
        if profile.count() == 0:
            return JsonResponse(
                create_json('post', 'جزئیات حساب کاربری', 'ناموفق', f'حساب کاربری یافت نشد'))
        serializer = ProfileSerializer(profile, many=True)
        result_data = serializer.data
        for data in result_data:
            data['email'] = request.user.email
        json_response_body = {
            'method': 'post',
            'request': 'جزئیات حساب کاربری',
            'result': 'موفق',
            'data': result_data,
        }
        return JsonResponse(json_response_body)

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


