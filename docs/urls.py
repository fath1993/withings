from django.urls import path

from docs.views import Docs

app_name = 'docs'

urlpatterns = [
    path('documentation/', Docs.as_view(), name='documentation'),
]