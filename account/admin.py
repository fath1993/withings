from django.contrib import admin
from account.models import Profile, SMSAuthCode


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'userid',
    )

    readonly_fields = (
        'user',
        'userid',
        'access_token',
        'refresh_token',
        'scope',
        'expiration_date',
        'token_type',

        'getmeas_data',
    )

    fields = (
        'user',
        'userid',
        'access_token',
        'refresh_token',
        'scope',
        'expiration_date',
        'token_type',

        'getmeas_data',
    )

    def has_add_permission(self, request):
        return False

