import json
import random
import uuid
from base64 import b64encode
from urllib.parse import urljoin

import jdatetime
import requests
from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from knox.models import AuthToken
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from django.contrib.auth.signals import user_logged_out
from accounts.models import Profile, SMSAuthCode
from accounts.serializer import ProfileSerializer
from accounts.utils import verified_signature_required, create_user_profile
from withings.settings import BASE_URL, WHITINGS_API_Endpoint, CLIENT_ID, SECRET, OAUTH2_CALLBACK_URL
from custom_logs.models import custom_log
from utilities.http_metod import fetch_data_from_http_post, fetch_single_file_from_http_files
from utilities.utilities import create_json


class AuthSimple(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'دریافت توکن با استفاده از نام کاربری و کلمه عبور'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                username = front_input['username']
                password = front_input['password']
                if username is None:
                    print('نام کاربری خالی است')
                    return JsonResponse(create_json('post', 'دریافت توکن', 'ناموفق', f'نام کاربری خالی است'))
                if password is None:
                    print('کلمه عبور خالی است')
                    return JsonResponse(create_json('post', 'دریافت توکن', 'ناموفق', f'کلمه عبور خالی است'))
                try:
                    user = User.objects.get(username=username)
                    user = authenticate(request=request, username=username, password=password)
                    if not user:
                        print('رمز عبور صحیح نیست')
                        return JsonResponse(create_json('post', 'دریافت توکن', 'ناموفق',
                                                        f'رمز عبور صحیح نیست'))
                    token = AuthToken.objects.create(user)
                    json_response_body = {
                        'method': 'post',
                        'request': 'دریافت توکن',
                        'result': 'موفق',
                        'token': token[1],
                        'message': f"این توکن به مدت {str(settings.REST_KNOX['TOKEN_TTL'])} روز اعتبار خواهد داشت"
                    }
                    return JsonResponse(json_response_body)
                except Exception as e:
                    print(str(e))
                    return JsonResponse(create_json('post', 'دریافت توکن', 'ناموفق',
                                                    f'نام کاربری ارائه شده با مقدار {username} در سامانه موجود نیست'))
            except Exception as e:
                print(str(e))
                return JsonResponse(
                    create_json('post', 'دریافت توکن', 'ناموفق', f'نام کاربری یا رمز عبور بدرستی ارسال نشده است '))
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'دریافت توکن', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class AuthEliminateALL(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'ابطال توکن های فعال کاربر'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                eliminate_all = front_input['eliminate_all']
                if eliminate_all is None:
                    print('نوع ابطال مشخص نشده است')
                    return JsonResponse(create_json('post', 'ابطال توکن', 'ناموفق', f'نوع ابطال مشخص نشده است'))
                eliminate_all = str(eliminate_all).lower()
                if eliminate_all == 'true' or eliminate_all == 'false':
                    print('نوع ابطال مشخص نشده است')
                    if eliminate_all == 'true':
                        try:
                            request._auth.delete()
                            user_logged_out.send(sender=request.user.__class__,
                                                 request=request, user=request.user)
                        except:
                            pass
                    else:
                        try:
                            request.user.auth_token_set.all().delete()
                            user_logged_out.send(sender=request.user.__class__,
                                                 request=request, user=request.user)
                        except:
                            pass
                    json_response_body = {
                        'method': 'post',
                        'request': 'ابطال توکن',
                        'result': 'موفق',
                        'eliminate_all': eliminate_all,
                    }
                    return JsonResponse(json_response_body)
                else:
                    print('تنها عبارات true یا false برای نوع ابطال مجاز می باشد')
                    return JsonResponse(create_json('post', 'ابطال توکن', 'ناموفق',
                                                    f'تنها عبارات true یا false برای نوع ابطال مجاز می باشد'))
            except Exception as e:
                print(str(e))
                return JsonResponse(
                    create_json('post', 'ابطال توکن', 'ناموفق', f'ورودی صحیح نیست یا بدرستی ارسال نشده است '))
        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'ابطال توکن', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


class Account(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'عملیات حساب کاربری'}

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

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
        try:
            front_input = json.loads(request.body)
            try:
                phone_number = front_input['phone_number']
            except:
                phone_number = None
            try:
                password = front_input['password']
            except:
                password = None
            try:
                email = front_input['email']
            except:
                email = None
            try:
                birthday = front_input['birthday']
            except:
                birthday = None
            user = request.user
            profile = user.user_profile
            if password:
                if password == '':
                    print('کلمه عبور خالی است')
                    return JsonResponse(
                        create_json('post', 'درخواست ویرایش اطلاعات حساب', 'ناموفق', f'کلمه عبور خالی است'))
                if len(str(password)) < 8:
                    print('کلمه عبور کمتر از 8 کاراکتر است')
                    return JsonResponse(create_json('post', 'درخواست ویرایش اطلاعات حساب', 'ناموفق',
                                                    f'کلمه عبور کمتر از 8 کاراکتر است'))
                user.set_password(str(password))
            if email:
                user.email = email
            user.save()
            if phone_number:
                profile.mobile_phone_number = phone_number
            if birthday:
                print(birthday)
                try:
                    birthday = str(birthday).split('/')
                    birthday = jdatetime.datetime(year=int(birthday[0]), month=int(birthday[1]),
                                                  day=int(birthday[2]))
                    profile.birthday = birthday
                except Exception as e:
                    print(e)
                    print('تاریخ تولد بدرستی ارسال نشده است')
                    return JsonResponse(create_json('post', 'درخواست ویرایش اطلاعات حساب', 'ناموفق',
                                                    f'تاریخ تولد ارسالی با مقدار {birthday} صحیح نیست'))
            profile.save()

            profile = Profile.objects.filter(user=request.user)
            if profile.count() == 0:
                return JsonResponse(
                    create_json('post', 'ویرایش حساب کاربری', 'ناموفق', f'حساب کاربری یافت نشد'))
            serializer = ProfileSerializer(profile, many=True)
            result_data = serializer.data
            for data in result_data:
                data['email'] = request.user.email
            json_response_body = {
                'method': 'put',
                'request': 'ویرایش حساب کاربری',
                'result': 'موفق',
                'data': serializer.data,
            }
            return JsonResponse(json_response_body)

        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'درخواست ویرایش اطلاعات حساب', 'ناموفق', f'ورودی صحیح نیست.'))

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        json_response_body = {
            'method': 'post',
            'request': 'حذف حساب کاربری',
            'result': 'موفق',
        }
        return JsonResponse(json_response_body)


def index(request):
    context = {}
    if request.user and request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')
    return render(request, 'index.html', context)


@api_view(['GET', 'POST'])
@verified_signature_required
def webhook_listen(request):
    # Subscription verification process
    # Reference: https://dev.fitbit.com/build/reference/web-api/subscriptions/#verify-a-subscriber
    code = request.GET.get('verify')
    if code:
        if code == settings.FITBIT_SUBSCRIBER_VERIFICATION_CODE:
            return JsonResponse({'message': 'HTTP_204_NO_CONTENT'})
        return JsonResponse({'message': 'HTTP_404_NO_CONTENT'})
    return JsonResponse({'message': 'HTTP_204_NO_CONTENT'})


@api_view(('GET',))
def get_profile(request, **kwargs):
    user = get_object_or_404(User, id=kwargs.get('id'))
    try:
        client = user.fb_auth.client
        return JsonResponse({'message': f'{client.user_profile_get(user.username).get('user')}'})
    except Exception as e:
        return JsonResponse({'message': 'User Not found'})


def auth_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    custom_log(f'Unable to login with given credentials. Please try again.')
    return redirect(index)


def auth_logout(request):
    logout(request)
    return redirect('index')


@user_passes_test(lambda user: user.is_superuser)
def auth_initialize(request):
    url = f'https://account.withings.com/oauth2_user/authorize2?response_type=code&client_id={CLIENT_ID}&scope=user.info,user.metrics,user.activity&redirect_uri={OAUTH2_CALLBACK_URL}&state=123456'
    request = requests.get(url)
    print(request.content)
    return redirect(request.url)


@api_view(['GET'])
def auth_complete(request):
    code = request.GET.get('code')
    url = urljoin(WHITINGS_API_Endpoint, 'oauth2/token')
    token_data = bytes(f'{CLIENT_ID}:'
                       f'{SECRET}', 'utf-8')
    token = b64encode(token_data).decode('utf-8')
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'grant_type': 'authorization_code',
        'code': code
    }
    try:
        credentials = requests.post(url, data=data, headers=headers).json()
        user_id = credentials.get('user_id')
        new_user = create_user_profile(credentials)
        profile = new_user.client.user_profile_get(user_id).get('user')
    except Exception as e:
        return JsonResponse({'message': f'HTTP_400_BAD_REQUEST. err: {e}'})
    return redirect('dashboard')

