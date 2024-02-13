import jdatetime
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect

from custom_logs.models import custom_log
from website.templatetags.website_custom_tags import has_user_active_token
from withings.settings import CLIENT_ID, SECRET


def index_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    else:
        if has_user_active_token(request.user):
            refresh_token_url = 'https://wbsapi.withings.net/v2/oauth2'

            payload = {
                'action': 'requesttoken',
                'grant_type': 'refresh_token',
                'client_id': f'{CLIENT_ID}',
                'client_secret': f'{SECRET}',
                'refresh_token': f'{request.user.user_profile.refresh_token}'
            }
            custom_log(str(payload))

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
        return render(request, 'index.html', context)


def ajax_fetch_data_from_withings_measure_view(request):
    if request.user.is_authenticated:
        if has_user_active_token(request.user):
            endpoint_url = 'https://wbsapi.withings.net/measure'

            headers = {
                'Authorization': f'Bearer {request.user.user_profile.access_token}'
            }

            data = {
                "action": "getmeas",
                "meastypes": "1,4",
                # "meastypes": "1,4,5,6,8,9,10,11,12,54,71,73,76,77,88,91,123,130,135,136,137,138,139,155,167,168,169,170,174,175,196",
                "category": "1",  # or 2.  1 for real measures, 2 for user objectives.
                # "startdate": "",
                # "enddate": "",
                # "lastupdate": "",
                # "offset": "",
            }

            data_guide = {
                "1": "Weight (kg)",
                "4": "Height (meter)",
                "5": "Fat Free Mass (kg)",
                "6": "Fat Ratio (%)",
                "8": "Fat Mass Weight (kg)",
                "9": "Diastolic Blood Pressure (mmHg)",
                "10": "Systolic Blood Pressure (mmHg)",
                "11": "Heart Pulse (bpm) - only for BPM and scale devices",
                "12": "Temperature (celsius)",
                "54": "SP02 (%)",
                "71": "Body Temperature (celsius)",
                "73": "Skin Temperature (celsius)",
                "76": "Muscle Mass (kg)",
                "77": "Hydration (kg)",
                "88": "Bone Mass (kg)",
                "91": "Pulse Wave Velocity (m/s)",
                "123": "VO2 max is a numerical measurement of your body’s ability to consume oxygen (ml/min/kg).",
                "130": "Atrial fibrillation result",
                "135": "QRS interval duration based on ECG signal",
                "136": "PR interval duration based on ECG signal",
                "137": "QT interval duration based on ECG signal",
                "138": "Corrected QT interval duration based on ECG signal",
                "139": "Atrial fibrillation result from PPG",
                "155": "Vascular age",
                "167": "Nerve Health Score Conductance 2 electrodes Feet",
                "168": "Extracellular Water in kg",
                "169": "Intracellular Water in kg",
                "170": "Visceral Fat (without unity)",
                "174": "Fat Mass for segments in mass unit",
                "175": "Muscle Mass for segments",
                "196": "Electrodermal activity feet",
            }
            try:
                response = requests.get(endpoint_url, headers=headers, data=data)
                if response.status_code == 200:
                    data = response.json()

                    # sample response at: https://developer.withings.com/api-reference#tag/measure/operation/measure-getmeas

                    profile = request.user.user_profile
                    profile.getmeas_data = data
                    profile.save()
                    return JsonResponse(data)
                else:
                    return JsonResponse({"message": f"response.status_code == {response.status_code}"})
            except Exception as e:
                return JsonResponse({"message": f"exception happens. err: {e}"})
        else:
            return JsonResponse({"message": "nothings"})
    else:
        return redirect('accounts:login')
