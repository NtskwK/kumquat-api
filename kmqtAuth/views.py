# Create your views here.

from rest_framework import viewsets
from rest_framework.response import Response

from kmqtAuth.models import Member
from kmqtAuth.serializers import MemberSerializer


class UserInfoViewSet(viewsets.ViewSet):
    queryset = Member.objects.all().order_by('-date_joined')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        user_info = Member.objects.filter(id=request.user.id) \
            .values('roles', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login')[0]

        role = request.user.roles

        match role:
            case 0:
                user_info['roles'] = ['amdin']
            case 1:
                user_info['roles'] = ['user']
            case _:
                user_info['roles'] = ['guest']

        return Response(user_info)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('-date_joined')
    serializer_class = MemberSerializer
    http_method_names = ['get']
