import json
from datetime import datetime, timedelta
import requests
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from account.custom_decorator import CheckLogin
from account.models import Profile
from account.serializer import ProfileSerializer
from custom_logs.models import custom_log
from utilities.http_metod import fetch_data_from_http_post, fetch_data_from_http_get
from utilities.utilities import create_json
from website.templatetags.website_custom_tags import has_user_active_token, fitbit_has_user_active_token, \
    fitbit_has_user_token, has_user_token


class ServiceApiView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def post(self, request, *args, **kwargs):
        try:
            front_input = json.loads(request.body)
            try:
                request_data = front_input['request_data']
                allowed_request_data_list = ['patients', 'patient',
                                             'fitbit_fetch_heart_rate_time_series_by_date',
                                             'fitbit_fetch_heart_rate_time_series_by_date_range',
                                             'fitbit_fetch_spO2_summary_by_date',
                                             'fitbit_fetch_spO2_summary_by_date_range',
                                             'fitbit_fetch_sleep_log_by_date',
                                             'fitbit_fetch_sleep_log_by_date_range',
                                             'fitbit_fetch_body_time_series_by_date',
                                             'fitbit_fetch_body_time_series_by_date_range',
                                             'withings_weight',
                                             'withings_fat_free_mass',
                                             'withings_fat_ratio',
                                             'withings_fat_mass_weight',
                                             'withings_muscle_mass',
                                             'withings_bone_mass', ]
                if not request_data in allowed_request_data_list:
                    return JsonResponse(
                        create_json('post', 'دریافت داده', 'ناموفق', f'داده درخواستی مورد پذیرش نیست'))

                if request_data == 'patients':
                    profiles = Profile.objects.filter()
                    serializer = ProfileSerializer(profiles, many=True)
                    json_response_body = {
                        "method": "post",
                        "request": "patients",
                        "result": "موفق",
                        "message": serializer.data,

                    }
                    return JsonResponse(json_response_body)
            except:
                return JsonResponse(
                    create_json('post', 'دریافت داده', 'ناموفق', f'مقدار request_data ارسال نشده است'))

            try:
                patient_id = front_input['patient_id']
                profiles = Profile.objects.filter(id=patient_id)
                if profiles.count() == 0:
                    return JsonResponse(
                        create_json('post', 'دریافت داده', 'ناموفق', f'بیمار با ایدی {patient_id} یافت نشد'))

                if request_data == 'patient':
                    serializer = ProfileSerializer(profiles, many=True)
                    json_response_body = {
                        "method": "post",
                        "request": "patients",
                        "result": "موفق",
                        "message": serializer.data,

                    }
                    return JsonResponse(json_response_body)

                user = profiles[0].user
                if has_user_token(user):
                    if not has_user_active_token(user):
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'توکن ویتینگر برای بیمار با ایدی {patient_id} منقضی شده است'))
                else:
                    return JsonResponse(
                        create_json('post', 'دریافت داده', 'ناموفق',
                                    f'توکن ویتینگز برای بیمار با ایدی {patient_id} وجود ندارد'))

                if fitbit_has_user_token(user):
                    if not fitbit_has_user_active_token(user):
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'توکن فیتبیت برای بیمار با ایدی {patient_id} منقضی شده است'))
                else:
                    return JsonResponse(
                        create_json('post', 'دریافت داده', 'ناموفق',
                                    f'توکن فیتبیت برای بیمار با ایدی {patient_id} وجود ندارد'))

                if request_data == 'fitbit_fetch_heart_rate_time_series_by_date':
                    try:
                        date = front_input['date']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date ارسال نشده است'))
                    try:
                        period = front_input['period']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار period ارسال نشده است'))
                    return fitbit_fetch_heart_rate_time_series_by_date(user, date, period)

                if request_data == 'fitbit_fetch_heart_rate_time_series_by_date_range':
                    try:
                        date_from = front_input['date_from']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date_from ارسال نشده است'))
                    try:
                        date_to = front_input['date_to']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date_to ارسال نشده است'))
                    return fitbit_fetch_heart_rate_time_series_by_date_range(user, date_from, date_to)

                if request_data == 'fitbit_fetch_spO2_summary_by_date':
                    try:
                        date = front_input['date']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date ارسال نشده است'))
                    return fitbit_fetch_spO2_summary_by_date(user, date)

                if request_data == 'fitbit_fetch_spO2_summary_by_date_range':
                    try:
                        date_from = front_input['date_from']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date_from ارسال نشده است'))
                    try:
                        date_to = front_input['date_to']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date_to ارسال نشده است'))
                    return fitbit_fetch_spO2_summary_by_date_range(user, date_from, date_to)

                if request_data == 'fitbit_fetch_sleep_log_by_date':
                    try:
                        date = front_input['date']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date ارسال نشده است'))
                    return fitbit_fetch_sleep_log_by_date(user, date)

                if request_data == 'fitbit_fetch_sleep_log_by_date_range':
                    try:
                        date_from = front_input['date_from']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date_from ارسال نشده است'))
                    try:
                        date_to = front_input['date_to']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date_to ارسال نشده است'))
                    return fitbit_fetch_sleep_log_by_date_range(user, date_from, date_to)

                if request_data == 'fitbit_fetch_body_time_series_by_date':
                    try:
                        resource = front_input['resource']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار resource ارسال نشده است'))
                    try:
                        date = front_input['date']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date ارسال نشده است'))
                    try:
                        period = front_input['period']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار period ارسال نشده است'))
                    return fitbit_fetch_body_time_series_by_date(user, resource, date, period)

                if request_data == 'fitbit_fetch_body_time_series_by_date_range':
                    try:
                        resource = front_input['resource']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار resource ارسال نشده است'))
                    try:
                        date_from = front_input['date_from']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date_from ارسال نشده است'))
                    try:
                        date_to = front_input['date_to']
                    except:
                        return JsonResponse(
                            create_json('post', 'دریافت داده', 'ناموفق',
                                        f'مقدار date_to ارسال نشده است'))
                    return fitbit_fetch_body_time_series_by_date_range(user, resource, date_from, date_to)

                try:
                    date_from = front_input['date_from']
                    date_from = get_date_timestamp(date_from)
                except:
                    date_from = None
                try:
                    date_to = front_input['date_to']
                    date_to = get_date_timestamp(date_to)
                except:
                    date_to = None

                if request_data == 'withings_weight':
                    return withings_fetch_weight(user, date_from, date_to)
                if request_data == 'withings_fat_free_mass':
                    return withings_fetch_fat_free_mass(user, date_from, date_to)
                if request_data == 'withings_fat_ratio':
                    return withings_fetch_fat_ratio(user, date_from, date_to)
                if request_data == 'withings_fat_mass_weight':
                    return withings_fetch_fat_mass_weight(user, date_from, date_to)
                if request_data == 'withings_muscle_mass':
                    return withings_fetch_muscle_mass(user, date_from, date_to)
                if request_data == 'withings_bone_mass':
                    return withings_fetch_bone_mass(user, date_from, date_to)
            except Exception as e:
                custom_log(e)
                return JsonResponse(
                    create_json('post', 'دریافت داده', 'ناموفق', f'مقدار patient_id ارسال نشده است'))

        except Exception as e:
            print(str(e))
            return JsonResponse(create_json('post', 'دریافت داده', 'ناموفق', f'ورودی صحیح نیست.'))

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})


def withings_fetch_weight(user, date_from: None, date_to: None):
    endpoint_url = 'https://wbsapi.withings.net/measure'

    headers = {
        'Authorization': f'Bearer {user.user_profile.access_token}'
    }

    if date_from and date_to:
        data = {
            "action": "getmeas",
            "meastype": "1",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
        }
    else:
        data = {
            "action": "getmeas",
            "meastype": "1",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
            "startdate": date_from,
            "enddate": date_to,
        }

    try:
        response = requests.get(endpoint_url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"message": f"response.status_code == {response.status_code}"})
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def withings_fetch_fat_free_mass(user, date_from: None, date_to: None):
    endpoint_url = 'https://wbsapi.withings.net/measure'

    headers = {
        'Authorization': f'Bearer {user.user_profile.access_token}'
    }

    if date_from and date_to:
        data = {
            "action": "getmeas",
            "meastype": "5",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
        }
    else:
        data = {
            "action": "getmeas",
            "meastype": "5",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
            "startdate": date_from,
            "enddate": date_to,
        }

    try:
        response = requests.get(endpoint_url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"message": f"response.status_code == {response.status_code}"})
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def withings_fetch_fat_ratio(user, date_from: None, date_to: None):
    endpoint_url = 'https://wbsapi.withings.net/measure'

    headers = {
        'Authorization': f'Bearer {user.user_profile.access_token}'
    }

    if date_from and date_to:
        data = {
            "action": "getmeas",
            "meastype": "6",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
        }
    else:
        data = {
            "action": "getmeas",
            "meastype": "6",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
            "startdate": date_from,
            "enddate": date_to,
        }

    try:
        response = requests.get(endpoint_url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"message": f"response.status_code == {response.status_code}"})
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def withings_fetch_fat_mass_weight(user, date_from: None, date_to: None):
    endpoint_url = 'https://wbsapi.withings.net/measure'

    headers = {
        'Authorization': f'Bearer {user.user_profile.access_token}'
    }

    if date_from and date_to:
        data = {
            "action": "getmeas",
            "meastype": "8",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
        }
    else:
        data = {
            "action": "getmeas",
            "meastype": "8",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
            "startdate": date_from,
            "enddate": date_to,
        }

    try:
        response = requests.get(endpoint_url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"message": f"response.status_code == {response.status_code}"})
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def withings_fetch_muscle_mass(user, date_from: None, date_to: None):
    endpoint_url = 'https://wbsapi.withings.net/measure'

    headers = {
        'Authorization': f'Bearer {user.user_profile.access_token}'
    }

    if date_from and date_to:
        data = {
            "action": "getmeas",
            "meastype": "76",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
        }
    else:
        data = {
            "action": "getmeas",
            "meastype": "76",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
            "startdate": date_from,
            "enddate": date_to,
        }

    try:
        response = requests.get(endpoint_url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()

            # sample response at: https://developer.withings.com/api-reference#tag/measure/operation/measure-getmeas
            #
            # profile = request.user.user_profile
            # profile.getmeas_data = data
            # profile.save()
            return JsonResponse(data)
        else:
            return JsonResponse({"message": f"response.status_code == {response.status_code}"})
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def withings_fetch_bone_mass(user, date_from: None, date_to: None):
    endpoint_url = 'https://wbsapi.withings.net/measure'

    headers = {
        'Authorization': f'Bearer {user.user_profile.access_token}'
    }

    if date_from and date_to:
        data = {
            "action": "getmeas",
            "meastype": "88",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
        }
    else:
        data = {
            "action": "getmeas",
            "meastype": "88",
            "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
            "startdate": date_from,
            "enddate": date_to,
        }

    try:
        response = requests.get(endpoint_url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"message": f"response.status_code == {response.status_code}"})
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def fitbit_fetch_body_time_series_by_date(user, resource, date, period):
    endpoint_url = f'https://api.fitbit.com/1/user/{user.user_profile.fitbit_userid}/body/{resource}/date/{date}/{period}.json'

    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        data = response.json()
        custom_log(f"fitbit_fetch_weight_view: {str(data)}")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def fitbit_fetch_body_time_series_by_date_range(user, resource, date_from, date_to):
    endpoint_url = f'https://api.fitbit.com/1/user/{user.user_profile.fitbit_userid}/body/{resource}/date/{date_from}/{date_to}.json'

    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        data = response.json()
        custom_log(f"fitbit_fetch_weight_view: {str(data)}")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def fitbit_fetch_sleep_log_by_date(user, date):
    endpoint_url = f'https://api.fitbit.com/1.2/user/{user.user_profile.fitbit_userid}/sleep/date/{date}.json'
    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        data = response.json()
        custom_log(f"fitbit_fetch_sleep_view: {str(data)}")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def fitbit_fetch_sleep_log_by_date_range(user, date_from, date_to):
    endpoint_url = f'https://api.fitbit.com/1.2/user/{user.user_profile.fitbit_userid}/sleep/date/{date_from}/{date_to}.json'
    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        data = response.json()
        custom_log(f"fitbit_fetch_sleep_view: {str(data)}")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"message": f"exception happens. err: {e}"})


def fitbit_fetch_spO2_summary_by_date(user, date):
    endpoint_url = f'https://api.fitbit.com/1/user/{user.user_profile.fitbit_userid}/spo2/date/{date}.json'
    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        data = response.json()
        custom_log(f"fitbit_fetch_spO2_view: {str(data)}")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse(
            {"message": f"exception happens. err: {e}"})


def fitbit_fetch_spO2_summary_by_date_range(user, date_from, date_to):
    endpoint_url = f'https://api.fitbit.com/1/user/{user.user_profile.fitbit_userid}/spo2/date/{date_from}/{date_to}.json'
    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        data = response.json()
        custom_log(f"fitbit_fetch_spO2_view: {str(data)}")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse(
            {"message": f"exception happens. err: {e}"})


def fitbit_fetch_heart_rate_time_series_by_date_range(user, date_from, date_to):
    endpoint_url = f'https://api.fitbit.com/1/user/{user.user_profile.fitbit_userid}/activities/heart/date/{date_from}/{date_to}.json'
    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        data = response.json()
        custom_log(f"fitbit_fetch_heart_rate_view: {str(data)}")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse(
            {"message": f"exception happens. err: {e}"})


def fitbit_fetch_heart_rate_time_series_by_date(user, date, period):
    endpoint_url = f'https://api.fitbit.com/1/user/{user.user_profile.fitbit_userid}/activities/heart/date/{date}/{period}.json'
    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        data = response.json()
        custom_log(f"fitbit_fetch_heart_rate_view: {str(data)}")
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse(
            {"message": f"exception happens. err: {e}"})


class DashboardView:

    def __init__(self):
        super().__init__()

    @CheckLogin()
    def landing(self, request, *args, **kwargs):
        context = {'page_title': 'landing'}
        # if fitbit_has_user_token(request.user):
        #     if fitbit_has_user_active_token(request.user):
        #         return redirect('website:landing')
        # if has_user_token(request.user):
        #     if has_user_active_token(request.user):
        #         return redirect('website:witings')
        # return render(request, 'landing.html', context)
        return render(request, 'landing.html', context)

    @CheckLogin()
    def dashboard(self, request, *args, **kwargs):
        context = {'page_title': 'Dashboard'}

        if fitbit_has_user_token(request.user):
            if fitbit_has_user_active_token(request.user):
                pass
            else:
                context['error'] = 'fitbit_has_user_active_token false'
                return render(request, 'landing.html', context)
        else:
            context['error'] = 'fitbit_has_user_token false'
            return render(request, 'landing.html', context)

        if has_user_token(request.user):
            if has_user_active_token(request.user):
                if not witings_token_is_active(request.user):
                    context['error'] = 'witings_has_user_active_token false'
                    return render(request, 'landing.html', context)
            else:
                context['error'] = 'witings_has_user_active_token false'
                return render(request, 'landing.html', context)
        else:
            context['error'] = 'witings_has_user_token false'
            return render(request, 'landing.html', context)

        return render(request, 'landing.html', context)


def witings_token_is_active(user):
    endpoint_url = 'https://wbsapi.withings.net/measure'

    headers = {
        'Authorization': f'Bearer {user.user_profile.access_token}'
    }

    data = {
        "action": "getmeas",
        "meastype": "1",
        "category": "1"
    }
    try:
        response = requests.get(endpoint_url, headers=headers, data=data)
        if response.status_code == 200:
            data = response.json()
            if str(data['status']) == '401':
                profile = user.user_profile
                profile.access_token = None
                profile.save()
                return False
            return True
        else:
            return False
    except Exception as e:
        return False


def fitbit_token_is_active(user):
    endpoint_url = f'https://api.fitbit.com/1/user/{user.user_profile.fitbit_userid}/body/log/weight/date/2024-03-23.json'

    headers = {
        'Authorization': f'Bearer {user.user_profile.fitbit_access_token}'
    }

    try:
        response = requests.get(endpoint_url, headers=headers)
        if response.status_code == 200:
            return True
        elif response.status_code == 429:
            return False
        elif response.status_code == 401:
            profile = user.user_profile
            profile.fitbit_access_token = None
            profile.save()
            return False
        else:
            return False
    except Exception as e:
        return False


def get_date_range_strf_time(date_range):
    now = datetime.now()
    if date_range == 'today':
        datetime_from = datetime(now.year, now.month, now.day, 0, 0, 0)
        datetime_to = datetime(now.year, now.month, now.day, 23, 59, 59)
    elif date_range == 'this_week':
        start_of_week = now - timedelta(days=now.weekday())
        datetime_from = datetime(start_of_week.year, start_of_week.month, start_of_week.day, 0, 0, 0)
        end_of_week = start_of_week + timedelta(days=6)
        datetime_to = datetime(end_of_week.year, end_of_week.month, end_of_week.day, 23, 59, 59)
    elif date_range == 'this_month':
        first_day_of_month = datetime(now.year, now.month, 1)
        datetime_from = datetime(first_day_of_month.year, first_day_of_month.month, first_day_of_month.day, 0, 0, 0)
        last_day_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)
        datetime_to = datetime(last_day_of_month.year, last_day_of_month.month, last_day_of_month.day, 23, 59, 59)
    else:
        # Default to all time
        datetime_from = datetime(year=2022, month=1, day=1, hour=0, minute=0)
        datetime_to = datetime.now()

    datetime_from_str = datetime_from.strftime('%Y-%m-%d')
    datetime_to_str = datetime_to.strftime('%Y-%m-%d')

    return datetime_from_str, datetime_to_str


def get_date_range_timestamp(date_range):
    now = datetime.now()
    if date_range == 'today':
        datetime_from = datetime(now.year, now.month, now.day, 0, 0, 0)
        datetime_to = datetime(now.year, now.month, now.day, 23, 59, 59)
    elif date_range == 'this_week':
        start_of_week = now - timedelta(days=now.weekday())
        datetime_from = datetime(start_of_week.year, start_of_week.month, start_of_week.day, 0, 0, 0)
        end_of_week = start_of_week + timedelta(days=6)
        datetime_to = datetime(end_of_week.year, end_of_week.month, end_of_week.day, 23, 59, 59)
    elif date_range == 'this_month':
        first_day_of_month = datetime(now.year, now.month, 1)
        datetime_from = datetime(first_day_of_month.year, first_day_of_month.month, first_day_of_month.day, 0, 0, 0)
        last_day_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)
        datetime_to = datetime(last_day_of_month.year, last_day_of_month.month, last_day_of_month.day, 23, 59, 59)
    else:
        # Default to all time
        datetime_from = 0
        datetime_to = 0

    try:
        datetime_from_ts = int(datetime_from.timestamp())
        datetime_to_ts = int(datetime_to.timestamp())
    except:
        datetime_from_ts = 0
        datetime_to_ts = 0

    return datetime_from_ts, datetime_to_ts


def get_date_timestamp(date):
    date = str(date).split('-')
    year = date[0]
    month = date[1]
    day = date[2]

    date_time = datetime(year=int(year), month=int(month), day=int(day))
    date_time_ts = int(date_time.timestamp())
    return date_time_ts
