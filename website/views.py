import json
import time
from datetime import datetime, timedelta
import requests
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from custom_logs.models import custom_log
from utilities.http_metod import fetch_data_from_http_post, fetch_data_from_http_get
from website.templatetags.website_custom_tags import has_user_active_token, fitbit_has_user_active_token, \
    fitbit_has_user_token, has_user_token


def landing_view(request):
    context = {'page_title': 'landing'}
    if request.user.is_authenticated:
        if fitbit_has_user_token(request.user):
            if fitbit_has_user_active_token(request.user):
                return redirect('website:fitbit')
        if has_user_token(request.user):
            if has_user_active_token(request.user):
                return redirect('website:witings')
        return render(request, 'landing.html', context)
    return redirect('accounts:login')


@csrf_exempt
def filter_view(request):
    context = {'page_title': 'Advance Filter'}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            form_type = fetch_data_from_http_get(request, 'form_type', context)
            if form_type == 'fitbit':
                patient_id = fetch_data_from_http_get(request, 'patient_id', context)
                oxygen_range = fetch_data_from_http_get(request, 'oxygen_range', context)
                sleep_range = fetch_data_from_http_get(request, 'sleep_range', context)
                spo2_range = fetch_data_from_http_get(request, 'spo2_range', context)
                heart_rate_range = fetch_data_from_http_get(request, 'heart_rate_range', context)
                context['patient_id'] = patient_id
                context['oxygen_range'] = get_date_range_strf_time(oxygen_range)
                context['sleep_range'] = get_date_range_strf_time(sleep_range)
                context['spo2_range'] = get_date_range_strf_time(spo2_range)
                context['heart_rate_range'] = get_date_range_strf_time(heart_rate_range)
                if fitbit_has_user_token(request.user):
                    if fitbit_has_user_active_token(request.user):
                        return render(request, 'dash-fitbit.html', context)
                    else:
                        context['error'] = 'Please connect with fitbit again'
                        return render(request, 'landing.html', context)
                else:
                    context['error'] = 'Please connect with fitbit first'
                    return render(request, 'landing.html', context)
            elif form_type == 'withings':
                patient_id = fetch_data_from_http_get(request, 'patient_id', context)
                weight_range = fetch_data_from_http_get(request, 'weight_range', context)
                fat_free_mass_range = fetch_data_from_http_get(request, 'fat_free_mass_range', context)
                fat_ratio_range = fetch_data_from_http_get(request, 'fat_ratio_range', context)
                fat_mass_weight_range = fetch_data_from_http_get(request, 'fat_mass_weight_range', context)
                muscle_mass_range = fetch_data_from_http_get(request, 'muscle_mass_range', context)
                bone_mass_range = fetch_data_from_http_get(request, 'bone_mass_range', context)
                context['patient_id'] = patient_id
                context['weight_range'] = get_date_range_timestamp(weight_range)
                context['fat_free_mass_range'] = get_date_range_timestamp(fat_free_mass_range)
                context['fat_ratio_range'] = get_date_range_timestamp(fat_ratio_range)
                context['fat_mass_weight_range'] = get_date_range_timestamp(fat_mass_weight_range)
                context['muscle_mass_range'] = get_date_range_timestamp(muscle_mass_range)
                context['bone_mass_range'] = get_date_range_timestamp(bone_mass_range)
                if has_user_token(request.user):
                    if has_user_active_token(request.user):
                        if not witings_token_is_active(request.user):
                            context['error'] = 'Please connect with withings again'
                            return render(request, 'landing.html', context)
                        return render(request, 'dash-witings.html', context)
                    else:
                        context['error'] = 'Please connect with withings again'
                        return render(request, 'landing.html', context)
                else:
                    context['error'] = 'Please connect with withings first'
                    return render(request, 'landing.html', context)
            else:
                return render(request, 'filter.html', context)
        else:
            return redirect('website:landing')
    return redirect('accounts:login')


def fitbit_dash_view(request):
    context = {'page_title': 'Fitbit Dashboard'}
    if request.user.is_authenticated:
        if fitbit_has_user_token(request.user):
            if fitbit_has_user_active_token(request.user):
                context['patient_id'] = request.user.user_profile.fitbit_userid
                context['oxygen_range'] = get_date_range_strf_time('today')
                context['sleep_range'] = get_date_range_strf_time('today')
                context['spo2_range'] = get_date_range_strf_time('today')
                context['heart_rate_range'] = get_date_range_strf_time('today')
                return render(request, 'dash-fitbit.html', context)
            else:
                context['error'] = 'fitbit_has_user_active_token false'
                return render(request, 'landing.html', context)
        else:
            context['error'] = 'fitbit_has_user_token false'
            return render(request, 'landing.html', context)
    return redirect('accounts:login')


def witings_dash_view(request):
    context = {'page_title': 'Witings Dashboard'}
    if request.user.is_authenticated:
        if has_user_token(request.user):
            if has_user_active_token(request.user):
                if not witings_token_is_active(request.user):
                    return redirect('website:witings')
                context['patient_id'] = request.user.user_profile.userid
                context['weight_range'] = get_date_range_timestamp('today')
                context['fat_free_mass_range'] = get_date_range_timestamp('today')
                context['fat_ratio_range'] = get_date_range_timestamp('today')
                context['fat_mass_weight_range'] = get_date_range_timestamp('today')
                context['muscle_mass_range'] = get_date_range_timestamp('today')
                context['bone_mass_range'] = get_date_range_timestamp('today')
                return render(request, 'dash-witings.html', context)
            else:
                context['error'] = 'witings_has_user_active_token false'
                return render(request, 'landing.html', context)
        else:
            context['error'] = 'witings_has_user_token false'
            return render(request, 'landing.html', context)
    return redirect('accounts:login')


def withings_fetch_weight_view(request):
    context = {}
    if request.user.is_authenticated:
        if has_user_token(request.user):
            if has_user_active_token(request.user):
                endpoint_url = 'https://wbsapi.withings.net/measure'

                headers = {
                    'Authorization': f'Bearer {request.user.user_profile.access_token}'
                }

                date_from = fetch_data_from_http_post(request, 'date_from', context)
                date_to = fetch_data_from_http_post(request, 'date_to', context)

                custom_log(date_from)
                custom_log(date_to)

                data = {
                    "action": "getmeas",
                    "meastype": "1",
                    "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
                    # "startdate": date_from,
                    # "enddate": date_to,
                    # "lastupdate": "",
                    # "offset": "",
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
            else:
                return JsonResponse({"message": "has_user_active_token false"})
        else:
            return JsonResponse({"message": "has_user_token false"})
    else:
        return JsonResponse({"message": "login required"})


def withings_fetch_fat_free_mass_view(request):
    context = {}
    if request.user.is_authenticated:
        if has_user_token(request.user):
            if has_user_active_token(request.user):
                endpoint_url = 'https://wbsapi.withings.net/measure'

                headers = {
                    'Authorization': f'Bearer {request.user.user_profile.access_token}'
                }

                date_from = fetch_data_from_http_post(request, 'date_from', context)
                date_to = fetch_data_from_http_post(request, 'date_to', context)

                data = {
                    "action": "getmeas",
                    "meastype": "5",
                    "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
                    # "startdate": date_from,
                    # "enddate": date_to,
                    # "lastupdate": "",
                    # "offset": "",
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
            else:
                return JsonResponse({"message": "has_user_active_token false"})
        else:
            return JsonResponse({"message": "has_user_token false"})
    else:
        return JsonResponse({"message": "login required"})


def withings_fetch_fat_ratio_view(request):
    context = {}
    if request.user.is_authenticated:
        if has_user_token(request.user):
            if has_user_active_token(request.user):
                endpoint_url = 'https://wbsapi.withings.net/measure'

                headers = {
                    'Authorization': f'Bearer {request.user.user_profile.access_token}'
                }

                date_from = fetch_data_from_http_post(request, 'date_from', context)
                date_to = fetch_data_from_http_post(request, 'date_to', context)

                data = {
                    "action": "getmeas",
                    "meastype": "6",
                    "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
                    # "startdate": date_from,
                    # "enddate": date_to,
                    # "lastupdate": "",
                    # "offset": "",
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
            else:
                return JsonResponse({"message": "has_user_active_token false"})
        else:
            return JsonResponse({"message": "has_user_token false"})
    else:
        return JsonResponse({"message": "login required"})


def withings_fetch_fat_mass_weight_view(request):
    context = {}
    if request.user.is_authenticated:
        if has_user_token(request.user):
            if has_user_active_token(request.user):
                endpoint_url = 'https://wbsapi.withings.net/measure'

                headers = {
                    'Authorization': f'Bearer {request.user.user_profile.access_token}'
                }

                date_from = fetch_data_from_http_post(request, 'date_from', context)
                date_to = fetch_data_from_http_post(request, 'date_to', context)

                data = {
                    "action": "getmeas",
                    "meastype": "8",
                    "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
                    # "startdate": date_from,
                    # "enddate": date_to,
                    # "lastupdate": "",
                    # "offset": "",
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
            else:
                return JsonResponse({"message": "has_user_active_token false"})
        else:
            return JsonResponse({"message": "has_user_token false"})
    else:
        return JsonResponse({"message": "login required"})


def withings_fetch_muscle_mass_view(request):
    context = {}
    if request.user.is_authenticated:
        if has_user_token(request.user):
            if has_user_active_token(request.user):
                endpoint_url = 'https://wbsapi.withings.net/measure'

                headers = {
                    'Authorization': f'Bearer {request.user.user_profile.access_token}'
                }

                date_from = fetch_data_from_http_post(request, 'date_from', context)
                date_to = fetch_data_from_http_post(request, 'date_to', context)

                data = {
                    "action": "getmeas",
                    "meastype": "76",
                    "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
                    # "startdate": date_from,
                    # "enddate": date_to,
                    # "lastupdate": "",
                    # "offset": "",
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
            else:
                return JsonResponse({"message": "has_user_active_token false"})
        else:
            return JsonResponse({"message": "has_user_token false"})
    else:
        return JsonResponse({"message": "login required"})


def withings_fetch_bone_mass_view(request):
    context = {}
    if request.user.is_authenticated:
        if has_user_token(request.user):
            if has_user_active_token(request.user):
                endpoint_url = 'https://wbsapi.withings.net/measure'

                headers = {
                    'Authorization': f'Bearer {request.user.user_profile.access_token}'
                }

                date_from = fetch_data_from_http_post(request, 'date_from', context)
                date_to = fetch_data_from_http_post(request, 'date_to', context)

                data = {
                    "action": "getmeas",
                    "meastype": "88",
                    "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
                    # "startdate": date_from,
                    # "enddate": date_to,
                    # "lastupdate": "",
                    # "offset": "",
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
            else:
                return JsonResponse({"message": "has_user_active_token false"})
        else:
            return JsonResponse({"message": "has_user_token false"})
    else:
        return JsonResponse({"message": "login required"})


def ajax_fetch_weight_log_from_fitbit(request):
    context = {}
    if request.user.is_authenticated:
        user_profile = request.user.user_profile
        if fitbit_has_user_token(request.user):
            if fitbit_has_user_active_token(request.user):
                date = fetch_data_from_http_post(request, 'date', context)
                if not date:
                    date = datetime.datetime.now()
                else:
                    date = str(date).split('-')
                    date = datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
                date = date.strftime("%Y-%m-%d")
                endpoint_url = f'https://api.fitbit.com/1/user/{user_profile.fitbit_userid}/body/log/weight/date/{date}.json'

                headers = {
                    'Authorization': f'Bearer {user_profile.fitbit_access_token}'
                }

                try:
                    response = requests.get(endpoint_url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        custom_log(str(data))
                        return JsonResponse(data)
                    else:
                        return JsonResponse({"message": f"response.status_code == {response.status_code}"})
                except Exception as e:
                    return JsonResponse({"message": f"exception happens. err: {e}"})
            else:
                return JsonResponse({"message": "fitbit_has_user_active_token false"})
        else:
            return JsonResponse({"message": "fitbit_has_user_token - false"})
    else:
        return JsonResponse({"message": "login required"})


def ajax_fetch_sleep_log_from_fitbit(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            patient_id = fetch_data_from_http_post(request, 'patient_id', context)
            if patient_id:
                try:
                    user = User.objects.get(id=patient_id)
                except:
                    return JsonResponse({"message": "patient_id not exist"})
            else:
                user = request.user
        else:
            user = request.user

        user_profile = user.user_profile
        if fitbit_has_user_token(user):
            if fitbit_has_user_active_token(user):
                sleep_date = fetch_data_from_http_post(request, 'sleep_date', context)
                if not sleep_date:
                    date = datetime.datetime.now()
                else:
                    date = str(sleep_date).split('-')
                    date = datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
                date = date.strftime("%Y-%m-%d")
                endpoint_url = f'https://api.fitbit.com/1.2/user/{user_profile.fitbit_userid}/sleep/date/{date}.json'

                headers = {
                    'Authorization': f'Bearer {user_profile.fitbit_access_token}'
                }

                try:
                    response = requests.get(endpoint_url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        custom_log(str(data))
                        return JsonResponse(data)
                    else:
                        return JsonResponse({"message": f"response.status_code == {response.status_code}"})
                except Exception as e:
                    return JsonResponse({"message": f"exception happens. err: {e}"})
            else:
                return JsonResponse({"message": "fitbit_has_user_active_token false"})
        else:
            return JsonResponse({"message": "fitbit_has_user_token - false"})
    else:
        return JsonResponse({"message": "login required"})


def ajax_get_spO2_summary_by_date_from_fitbit(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            patient_id = fetch_data_from_http_post(request, 'patient_id', context)
            if patient_id:
                try:
                    user = User.objects.get(id=patient_id)
                except:
                    return JsonResponse({"message": "patient_id not exist"})
            else:
                user = request.user
        else:
            user = request.user
        user_profile = user.user_profile
        if fitbit_has_user_token(user):
            if fitbit_has_user_active_token(user):
                start_date = fetch_data_from_http_post(request, 'start_date', context)
                end_date = fetch_data_from_http_post(request, 'end_date', context)
                if not start_date:
                    start_date = datetime.datetime.now()
                else:
                    start_date = str(start_date).split('-')
                    start_date = datetime.datetime(year=int(start_date[0]), month=int(start_date[1]),
                                                   day=int(start_date[2]))
                if not end_date:
                    end_date = datetime.datetime.now()
                else:
                    end_date = str(end_date).split('-')
                    end_date = datetime.datetime(year=int(end_date[0]), month=int(end_date[1]), day=int(end_date[2]))
                start_date = start_date.strftime("%Y-%m-%d")
                end_date = end_date.strftime("%Y-%m-%d")
                custom_log(start_date)
                custom_log(end_date)
                endpoint_url = f'https://api.fitbit.com/1/user/{user_profile.fitbit_userid}/spo2/date/{start_date}/{end_date}.json'

                headers = {
                    'Authorization': f'Bearer {user_profile.fitbit_access_token}'
                }

                try:
                    response = requests.get(endpoint_url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        custom_log(str(data))
                        return JsonResponse(data, safe=False)
                    else:
                        return JsonResponse({
                                                "message": f"ajax_get_spO2_summary_by_date_from_fitbit response.status_code == {response.status_code}"})
                except Exception as e:
                    return JsonResponse(
                        {"message": f"ajax_get_spO2_summary_by_date_from_fitbit exception happens. err: {e}"})
            else:
                return JsonResponse({"message": "fitbit_has_user_active_token false"})
        else:
            return JsonResponse({"message": "fitbit_has_user_token - false"})
    else:
        return JsonResponse({"message": "login required"})


def ajax_get_heart_rate_time_series_by_date_from_fitbit(request):
    context = {}
    if request.user.is_authenticated:
        user_profile = request.user.user_profile
        if fitbit_has_user_token(request.user):
            if fitbit_has_user_active_token(request.user):
                date = fetch_data_from_http_post(request, 'date', context)
                period = fetch_data_from_http_post(request, 'period', context)
                if not date:
                    date = datetime.datetime.now()
                else:
                    date = str(date).split('-')
                    date = datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
                date = date.strftime("%Y-%m-%d")

                if not period:
                    period = '1d'

                endpoint_url = f'https://api.fitbit.com/1/user/{user_profile.fitbit_userid}/activities/heart/date/{date}/{period}.json'

                headers = {
                    'Authorization': f'Bearer {user_profile.fitbit_access_token}'
                }

                try:
                    response = requests.get(endpoint_url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        custom_log(str(data))
                        return JsonResponse(data)
                    else:
                        return JsonResponse({
                                                "message": f"ajax_get_spO2_summary_by_date_from_fitbit response.status_code == {response.status_code}"})
                except Exception as e:
                    return JsonResponse(
                        {"message": f"ajax_get_spO2_summary_by_date_from_fitbit exception happens. err: {e}"})
            else:
                return JsonResponse({"message": "fitbit_has_user_active_token false"})
        else:
            return JsonResponse({"message": "fitbit_has_user_token - false"})
    else:
        return JsonResponse({"message": "login required"})


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
        # Default to today
        datetime_from = datetime(now.year, now.month, now.day, 0, 0, 0)
        datetime_to = datetime(now.year, now.month, now.day, 23, 59, 59)

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
        # Default to today
        datetime_from = datetime(now.year, now.month, now.day, 0, 0, 0)
        datetime_to = datetime(now.year, now.month, now.day, 23, 59, 59)

    datetime_from_ts = int(datetime_from.timestamp())
    datetime_to_ts = int(datetime_to.timestamp())

    return datetime_from_ts, datetime_to_ts