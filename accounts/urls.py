from django.urls import path, include, re_path

from accounts.views import AuthSimple, AuthEliminateALL, Account, get_profile, auth_login, auth_logout, auth_initialize, \
    auth_complete

app_name = 'accounts'

urlpatterns = (
    # auth
    path('api/auth-simple/', AuthSimple.as_view(), name='api-auth-simple'),
    path('api/auth-eliminate-all/', AuthEliminateALL.as_view(), name='api-auth-eliminate-all'),

    # account
    path('api/account/', Account.as_view(), name='account'),

    re_path(r'users/(?P<id>\w+)/', get_profile, name='get-user-profile'),
    path('login/', auth_login, name='login'),
    path('logout/', auth_logout, name='logout'),
    path('fitbit-login/', auth_initialize, name='add-new-patient'),
    path('complete/', auth_complete, name='login-fitbit-complete'),
)
