from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from withings.settings import BASE_FRONT_URL


class Docs(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {'detail': 'داکیومنت ها'}

    def get(self, request, *args, **kwargs):
        json_response_body = {
            'راهنمایی استفاده از متد های REST': {
                'base': f'{BASE_FRONT_URL}',
                'api/service/': {
                    'درخواست': 'دریافت اطلاعات از سرویس',
                    'GET': {
                        'توضیحات': 'متد غیر مجاز',
                    },
                    'POST': {
                        'توضیحات': 'با استفاده از این متد امکان دریافت اطلاعات از سرویس بصورت REST فراهم شده است',
                        'سبک داده مورد پذیرش': 'json جیسون',
                        'جزئیات ارسال داده': {
                            'دیتای تمامی بیماران': {
                                'داده های ارسالی': {
                                    'request_data': 'patients',
                                },
                            },
                            'دیتای بیمار با ایدی مشخص': {
                                'داده های ارسالی': {
                                    'request_data': 'patient',
                                    'patient_id': 'آیدی بیمار',
                                },
                            },
                            'FitBit - Get Heart Rate Time Series by Date': {
                                'request_data': 'fitbit_fetch_heart_rate_time_series_by_date',
                                'patient_id': 'آیدی بیمار',
                                'date': 'yyyy-MM-dd,today',
                                'period': '1d,7d,30d,1w,1m',
                            },
                            'FitBit - Get Heart Rate Time Series by Date Range': {
                                'request_data': 'fitbit_fetch_heart_rate_time_series_by_date_range',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd,today',
                                'date_to': 'yyyy-MM-dd,today',
                            },
                            'FitBit - Get SpO2 Summary by Date': {
                                'request_data': 'fitbit_fetch_spO2_summary_by_date',
                                'patient_id': 'آیدی بیمار',
                                'date': 'yyyy-MM-dd,today',
                            },
                            'FitBit - Get SpO2 Summary by Date Range': {
                                'request_data': 'fitbit_fetch_spO2_summary_by_date_range',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd,today',
                                'date_to': 'yyyy-MM-dd,today',
                            },
                            'FitBit - Get Sleep Log by Date': {
                                'request_data': 'fitbit_fetch_sleep_log_by_date',
                                'patient_id': 'آیدی بیمار',
                                'date': 'yyyy-MM-dd,today',
                            },
                            'FitBit - Get Sleep Log by Date Range': {
                                'request_data': 'fitbit_fetch_sleep_log_by_date_range',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd,today',
                                'date_to': 'yyyy-MM-dd,today',
                            },
                            'FitBit - Get Body Time Series by Date': {
                                'request_data': 'fitbit_fetch_body_time_series_by_date',
                                'patient_id': 'آیدی بیمار',
                                'resource': 'bmi,fat,weight',
                                'date': 'yyyy-MM-dd,today',
                                'period': '1d,7d,30d,1w,1m,3m,6m,1y,max',
                            },
                            'FitBit - Get Body Time Series by Date Range': {
                                'request_data': 'fitbit_fetch_body_time_series_by_date_range',
                                'patient_id': 'آیدی بیمار',
                                'resource': 'bmi,fat,weight',
                                'date_from': 'yyyy-MM-dd,today',
                                'date_to': 'yyyy-MM-dd,today',
                            },
                            'Withings - Weight': {
                                'request_data': 'withings_fetch_weight',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd (not required)',
                                'date_to': 'yyyy-MM-dd (not required)',
                            },
                            'Withings - Fat Free Mass': {
                                'request_data': 'withings_fat_free_mass',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd (not required)',
                                'date_to': 'yyyy-MM-dd (not required)',
                            },
                            'Withings - Fat Ratio': {
                                'request_data': 'withings_fat_ratio',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd (not required)',
                                'date_to': 'yyyy-MM-dd (not required)',
                            },
                            'Withings - Fat Mass Weight': {
                                'request_data': 'withings_fat_mass_weight',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd (not required)',
                                'date_to': 'yyyy-MM-dd (not required)',
                            },
                            'Withings - Muscle Mass': {
                                'request_data': 'withings_muscle_mass',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd (not required)',
                                'date_to': 'yyyy-MM-dd (not required)',
                            },
                            'Withings - Bone Mass': {
                                'request_data': 'withings_bone_mass',
                                'patient_id': 'آیدی بیمار',
                                'date_from': 'yyyy-MM-dd (not required)',
                                'date_to': 'yyyy-MM-dd (not required)',
                            },
                        },
                        'داده بازگشتی در صورت موفقیت': {
                            'method': 'post',
                            'request': 'دریافت اطلاعات از سرویس',
                            'result': 'موفق',
                            'message': '[] for data or {} for error',
                        },
                    },
                    'PUT': {
                        'توضیحات': 'متد غیر مجاز',
                    },
                    'DELETE': {
                        'توضیحات': 'متد غیر مجاز',
                    },
                },
            }
        }
        return JsonResponse(json_response_body)

    def post(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def put(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})

    def delete(self, request, *args, **kwargs):
        return JsonResponse({'message': 'not allowed'})
