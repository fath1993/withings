from django.contrib import admin
from account.models import Profile, SMSAuthCode


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
    )

    readonly_fields = (
        'user',
    )

    fields = (
        'user',
        'birthday',
    )

    def has_add_permission(self, request):
        return False

