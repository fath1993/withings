import datetime

from rest_framework import serializers

from account.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in ret:
            if ret[field] is None:
                ret[field] = ""
        ret['username'] = instance.user.username
        ret['email'] = instance.user.email

        try:
            today = datetime.datetime.today()
            birthday = instance.birthday
            age = int(round(((today - birthday).total_seconds()) / (3600 * 24 * 360), 0))
            ret['age'] = age
        except:
            ret['age'] = ''

        return ret