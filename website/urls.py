from django.urls import path
from website.views import index_view, ajax_fetch_data_from_withings_measure_view

app_name = 'website'

urlpatterns = (
    path('', index_view, name='index'),

    # Ajax
    path('ajax/ajax-fetch-data-from-withings-measure/', ajax_fetch_data_from_withings_measure_view, name='ajax-fetch-data-from-withings-measure'),
)
