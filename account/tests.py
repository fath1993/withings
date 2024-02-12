import json

import requests
from django.test import TestCase

from withings.settings import BASE_DIR, BASE_URL


def test_auth_simple(username, password):
    url = f'{BASE_URL}account/api/auth-simple/'
    data = {
        'username': f'{username}',
        'password': f'{password}',
    }
    try:
        response = requests.post(url=url, json=data)
        print(json.loads(response.content))
    except Exception as e:
        print(str(e))


def test_auth_sms_request(phone_number):
    url = f'{BASE_URL}account/api/auth-sms-request/'
    data = {
        'phone_number': f'{phone_number}',
    }
    try:
        response = requests.post(url=url, json=data)
        print(json.loads(response.content))
    except Exception as e:
        print(str(e))


def test_auth_auth_sms_validate(phone_number, validate_code):
    url = f'{BASE_URL}account/api/auth-sms-validate/'
    data = {
        'phone_number': f'{phone_number}',
        'validate_code': f'{validate_code}',
    }
    try:
        response = requests.post(url=url, json=data)
        print(json.loads(response.content))
    except Exception as e:
        print(str(e))


def test_auth_eliminate_all(eliminate_all_1, user_active_token_1):
    url = f'{BASE_URL}account/api/auth-eliminate-all/'
    headers = {
        'Authorization': f'BatoboxToken {user_active_token_1}'
    }
    data = {
        'eliminate_all': f'{eliminate_all_1}',
    }
    try:
        response = requests.post(url=url, headers=headers, json=data)
        print(json.loads(response.content))
    except Exception as e:
        print(str(e))


def test_register():
    url = f'{BASE_URL}account/api/register/'
    data = {
        'phone_number': '09125502517',
        'password': 'amir1888',
        'first_name': 'امیرحسین',
        'last_name': 'فتح اللهی',
        'email': 'dj1372@gmail.com',
        'birthday': '1372/05/23',
        'province': 'تهران',
        'city': 'تهران',
        'address': 'تهران شریعتی',
        'zip_code': '1985258598',
    }
    try:
        response = requests.post(url=url, json=data)
        print(json.loads(response.content))
    except Exception as e:
        print(str(e))


def test_register_confirm(phone_number, verify_code):
    url = f'{BASE_URL}account/api/register-confirm/'
    data = {
        'phone_number': f'{phone_number}',
        'verify_code': f'{verify_code}',
    }
    try:
        response = requests.post(url=url, json=data)
        print(json.loads(response.content))
    except Exception as e:
        print(str(e))


def test_account(user_active_token, method_name):
    url = f'{BASE_URL}account/api/account/'
    headers = {
        'Authorization': f'BatoboxToken {user_active_token}'
    }
    if method_name == 'post':
        try:
            response = requests.post(url=url, headers=headers)
            print(json.loads(response.content))
        except Exception as e:
            print(str(e))
    elif method_name == 'put':
        data = {
            'first_name': 'امیرحسین',
            'last_name': 'بارانی',
            'birthday': '1372/05/23',
        }
        try:
            response = requests.put(url=url, headers=headers, json=data)
            print(json.loads(response.content))
        except Exception as e:
            print(str(e))
    elif method_name == 'delete':
        try:
            response = requests.delete(url=url, headers=headers)
            print(json.loads(response.content))
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    while True:
        print('please choose a number:')
        print('1. test_auth_simple')
        print('2. test_auth_sms_request')
        print('3. test_auth_auth_sms_validate')
        print('4. test_auth_eliminate_all')
        print('5. test_register')
        print('6. test_register_confirm')
        print('7. test_account')
        try:
            choice = int(input())
            if choice == 1:
                print('please input username:')
                username = str(input())
                print('please input password:')
                password = str(input())
                test_auth_simple(username, password)
            elif choice == 2:
                print('please input phone_number:')
                phone_number = str(input())
                test_auth_sms_request(phone_number)
            elif choice == 3:
                print('please input phone_number:')
                phone_number = str(input())
                print('please input validation code:')
                validation_code = str(input())
                test_auth_auth_sms_validate(phone_number, validation_code)
            elif choice == 4:
                print('please input user active token:')
                user_active_token = str(input())
                print('do you want to eliminate all session or current? true or false:')
                eliminate_all = str(input())
                if eliminate_all == 'true' or eliminate_all == 'false':
                    test_auth_eliminate_all(eliminate_all, user_active_token)
                else:
                    print('not correct! try again')
            elif choice == 5:
                print('the register will done with this: ')
                print({
                    'phone_number': '09125502517',
                    'password': 'amir1888',
                    'full_name': 'امیرحسین فتح اللهی',
                    'email': 'dj1372@gmail.com',
                    'birthday': '1372/05/23',
                    'province': 'تهران',
                    'city': 'تهران',
                    'address': 'تهران شریعتی',
                    'zip_code': '1985258598',
                    'profile_pic': 'default',
                })
                test_register()
            elif choice == 6:
                print('please input phone_number:')
                phone_number = str(input())
                print('please input validation code:')
                validation_code = str(input())
                test_register_confirm(phone_number, validation_code)
            elif choice == 7:
                print('please input user active token:')
                user_active_token = str(input())
                print('please input method name:')
                method_name = str(input())
                if method_name == 'post' or method_name == 'put' or method_name == 'delete':
                    test_account(user_active_token, method_name)
                else:
                    print('not correct! try again')
        except:
            print('not correct! try again')
