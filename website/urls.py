from django.urls import path
from website.views import DashboardView, ServiceApiView

app_name = 'website'

urlpatterns = (
    path('', DashboardView().landing, name='landing'),
    path('api/service/', ServiceApiView.as_view(), name='api-service'),
)


