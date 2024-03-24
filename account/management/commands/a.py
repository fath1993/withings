from django.core.management import base

from account.models import Profile
from account.tasks import auth_fitbit_refresh_token_view


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        profile = Profile.objects.get(user__username='admin')
        auth_fitbit_refresh_token_view(profile)