import jdatetime
from django import template

from custom_logs.models import custom_log

register = template.Library()


@register.filter
def has_user_active_token(user):
    try:
        if user.user_profile.access_token:
            if user.user_profile.expiration_date > jdatetime.datetime.now():
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(str(e))
        return False


@register.filter
def has_user_token(user):
    try:
        if user.user_profile.access_token:
            return True
        else:
            return False
    except Exception as e:
        print(str(e))
        return False