from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE, null=False, blank=False,
                                editable=False, verbose_name='user')
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='last name')
    sex = models.CharField(max_length=255, null=True, blank=True, verbose_name='sex')
    bmi = models.CharField(max_length=255, null=True, blank=True, verbose_name='bmi')
    weight = models.CharField(max_length=255, null=True, blank=True, verbose_name='weight')
    height = models.CharField(max_length=255, null=True, blank=True, verbose_name='height')
    birthday = models.DateTimeField(null=True, blank=True, verbose_name='birthday')
    userid = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='user id')
    access_token = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='access token')
    refresh_token = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='refresh token')
    scope = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='scope')
    expiration_date = jmodel.jDateTimeField(null=True, blank=True, editable=False, verbose_name='expiration date')
    token_type = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='token_type')
    getmeas_data = models.JSONField(null=True, blank=True, editable=False, verbose_name='getmeas data')

    fitbit_code_verifier = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='fitbit_code_verifier')
    fitbit_userid = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='user id')
    fitbit_access_token = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='access token')
    fitbit_refresh_token = models.CharField(max_length=255, null=True, blank=True, editable=False,
                                     verbose_name='refresh token')
    fitbit_scope = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='scope')
    fitbit_expiration_date = jmodel.jDateTimeField(null=True, blank=True, editable=False, verbose_name='expiration date')
    fitbit_token_type = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='token_type')
    fitbit_getmeas_data = models.JSONField(null=True, blank=True, editable=False, verbose_name='getmeas data')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


@receiver(post_save, sender=User)
def auto_create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

