from django.urls import path
from website.views import landing_view, filter_view, \
    fitbit_dash_view, witings_dash_view, \
    withings_fetch_weight_view, withings_fetch_fat_free_mass_view, \
    withings_fetch_fat_ratio_view, withings_fetch_fat_mass_weight_view, withings_fetch_muscle_mass_view, \
    withings_fetch_bone_mass_view, fitbit_fetch_weight_view, fitbit_fetch_sleep_view, fitbit_fetch_spO2_view, \
    fitbit_fetch_heart_rate_view

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

    # Fitbit
    path('fitbit-fetch-weight/', fitbit_fetch_weight_view, name='fitbit-fetch-weight'),
    path('fitbit-fetch-sleep/', fitbit_fetch_sleep_view, name='fitbit-fetch-sleep'),
    path('fitbit-fetch-spO2/', fitbit_fetch_spO2_view, name='fitbit-fetch-spO2'),
    path('fitbit-fetch-heart-rate/', fitbit_fetch_heart_rate_view, name='fitbit-fetch-heart-rate'),
)


