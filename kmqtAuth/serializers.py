from rest_framework import serializers

from kmqtAuth.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['roles', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login']