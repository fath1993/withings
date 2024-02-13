import jdatetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_jalali.db import models as jmodel


class SMSAuthCode(models.Model):
    phone_number = models.CharField(max_length=255, null=False, blank=False, editable=False,
                                    verbose_name='شماره موبایل')
    pass_code = models.CharField(max_length=255, null=False, blank=False, editable=False, verbose_name='کد احراز')
    created_at = jmodel.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.phone_number

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'کد تایید پیامکی'
        verbose_name_plural = 'کد های تایید پیامکی'


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE, null=False, blank=False,
                                editable=False, verbose_name='کاربر')
    userid = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='آیدی کاربر')
    access_token = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='توکن دسترسی')
    refresh_token = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='توکن بروز رسانی')
    scope = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='سطح دسترسی')
    expiration_date = jmodel.jDateTimeField(null=True, blank=True, editable=False, verbose_name='تاریخ انقضا')
    token_type = models.CharField(max_length=255, null=True, blank=True, editable=False, verbose_name='نوع توکن')

    getmeas_data = models.JSONField(null=True, blank=True, editable=False, verbose_name='getmeas data')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'


@receiver(post_save, sender=User)
def auto_create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

