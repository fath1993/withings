import datetime

import jdatetime
from django import template
from django.contrib.auth.models import User

from custom_logs.models import custom_log

register = template.Library()


@register.filter
def get_age(user):
    try:
        profile = user.user_profile

        today = datetime.datetime.today()
        birthday = profile.birthday

        age = int(round(((today - birthday).total_seconds()) / (3600 * 24 * 360), 0))
        return age
    except:
        return 0


@register.filter
def get_all_users(user):
    if user.is_superuser:
        all_users = User.objects.all()
        return all_users
    else:
        return User.objects.filter(id=user.id)


@register.filter
def get_patient(patient_id, arg):
    try:
        user = User.objects.get(id=patient_id)
        if str(arg) == 'first_name':
            return user.user_profile.first_name
        if str(arg) == 'last_name':
            return user.user_profile.last_name
        if str(arg) == 'age':
            return get_age(user)
        if str(arg) == 'sex':
            return user.user_profile.sex
    except Exception as e:
        custom_log(str(e))
        return None