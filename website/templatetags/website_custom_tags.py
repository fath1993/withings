import jdatetime
from django import template

register = template.Library()


@register.filter
def has_user_active_token(user):
    if user.user_profile.access_token:
        if user.user_profile.access_token.expiration_date > jdatetime.datetime.now():
            print(True)
            return True
        else:
            return False
    else:
        return False

