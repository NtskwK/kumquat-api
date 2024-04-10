from rest_framework import serializers

from kmqtAuth.models import KmqtUser


class KmqtUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KmqtUser
        fields = ['roles', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login', 'is_delete']


class CreateKmqtUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KmqtUser
        fields = ['username', 'password', 'email']

