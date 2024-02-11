from django.core.management import base

from accounts.tests import test_auth_simple, test_auth_sms_request, test_auth_auth_sms_validate, \
    test_auth_eliminate_all, test_register, test_register_confirm, test_account


class Command(base.BaseCommand):
    def handle(self, *args, **options):
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
