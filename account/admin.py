from django.contrib import admin
from account.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_name',
        'last_name',
        'sex',
        'bmi',
        'weight',
        'height',
        'userid',
        'fitbit_userid',
    )

    readonly_fields = (
        'user',

        'userid',
        'fitbit_userid',
        'access_token',
        'refresh_token',
        'scope',
        'expiration_date',
        'token_type',
        'getmeas_data',

        'fitbit_code_verifier',
        'fitbit_userid',
        'fitbit_access_token',
        'fitbit_refresh_token',
        'fitbit_scope',
        'fitbit_expiration_date',
        'fitbit_token_type',
        'fitbit_getmeas_data',
    )

    fields = (
        'user',
        'first_name',
        'last_name',
        'sex',
        'bmi',
        'weight',
        'height',
        'birthday',

        'userid',
        'access_token',
        'refresh_token',
        'scope',
        'expiration_date',
        'token_type',
        'getmeas_data',

        'fitbit_code_verifier',
        'fitbit_userid',
        'fitbit_access_token',
        'fitbit_refresh_token',
        'fitbit_scope',
        'fitbit_expiration_date',
        'fitbit_token_type',
        'fitbit_getmeas_data',
    )

    def has_add_permission(self, request):
        return False

