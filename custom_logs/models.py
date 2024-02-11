from django.db import models
from django_jalali.db import models as jmodels

LOG_LEVEL = (('DEBUG', 'DEBUG'), ('INFO', 'INFO'))


class CustomLog(models.Model):
    description = models.TextField(default='no description', null=False, blank=True, verbose_name='توضیحات ')
    log_level = models.CharField(default='INFO', max_length=255, choices=LOG_LEVEL, null=False, blank=False,
                                 verbose_name='سطح لوگ ')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان و تاریخ ایجاد')

    def __str__(self):
        return self.description[:50]

    class Meta:
        ordering = ['-created_at', ]
        verbose_name = 'لاگ'
        verbose_name_plural = 'لاگ ها'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if CustomLog.objects.all().count() > 5000:
            CustomLog.objects.filter(id__in=CustomLog.objects.filter().values_list('id').order_by('id')[:2500]).delete()


def custom_log(description: str, log_level: str = None):
    if not log_level:
        log_level = 'INFO'
    new_log = CustomLog(
        description=str(description),
        log_level=log_level,
    )
    new_log.save()
    print(str(description))
