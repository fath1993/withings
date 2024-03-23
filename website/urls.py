from django.urls import path
from website.views import landing_view, filter_view, ajax_fetch_weight_log_from_fitbit, \
    ajax_fetch_sleep_log_from_fitbit, fitbit_dash_view, witings_dash_view, ajax_get_spO2_summary_by_date_from_fitbit, \
    ajax_get_heart_rate_time_series_by_date_from_fitbit, withings_fetch_weight_view, withings_fetch_fat_free_mass_view, \
    withings_fetch_fat_ratio_view, withings_fetch_fat_mass_weight_view, withings_fetch_muscle_mass_view, \
    withings_fetch_bone_mass_view

app_name = 'website'

urlpatterns = (
    path('', landing_view, name='landing'),
    path('filter/', filter_view, name='filter'),
    path('fitbit/', fitbit_dash_view, name='fitbit'),
    path('witings/', witings_dash_view, name='witings'),

    # Witings
    path('withings-fetch-weight/', withings_fetch_weight_view, name='withings-fetch-weight'),
    path('withings-fetch-fat-free-mass/', withings_fetch_fat_free_mass_view,
         name='withings-fetch-fat-free-mass'),
    path('withings-fetch-fat-ratio/', withings_fetch_fat_ratio_view,
         name='withings-fetch-fat-ratio'),
    path('withings-fetch-fat-mass-weight/', withings_fetch_fat_mass_weight_view,
         name='withings-fetch-fat-mass-weight'),
    path('withings-fetch-muscle-mass/', withings_fetch_muscle_mass_view,
         name='withings-fetch-muscle-mass'),
    path('withings-fetch-bone-mass/', withings_fetch_bone_mass_view,
         name='withings-fetch-bone-mass'),

    # Ajax Fitbit
    path('ajax/ajax-fetch-weight-log-from-fitbit/', ajax_fetch_weight_log_from_fitbit, name='ajax/ajax-fetch-weight-log-from-fitbit'),
    path('ajax/ajax-fetch-sleep-log-from-fitbit/', ajax_fetch_sleep_log_from_fitbit, name='ajax/ajax-fetch-sleep-log-from-fitbit'),
    path('ajax/ajax-get-spO2-summary-by-date-from-fitbit/', ajax_get_spO2_summary_by_date_from_fitbit, name='ajax-get-spO2-summary-by-date-from-fitbit'),
    path('ajax/ajax-get-heart-rate-time-series-by-date-from-fitbit/', ajax_get_heart_rate_time_series_by_date_from_fitbit,
         name='ajax-get-heart-rate-time-series-by-date-from-fitbit'),
)


