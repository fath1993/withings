from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt

from account.views import auth_withings_view, auth_withings_callback_view, login_view, logout_view

app_name = 'accounts'

urlpatterns = (
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('auth-withings/', auth_withings_view, name='auth-withings'),
    path('auth2_callback/', csrf_exempt(auth_withings_callback_view), name='auth2_callback'),
)
