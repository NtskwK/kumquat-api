# Create your views here.
from datetime import datetime
from urllib.parse import urlparse, splitport

from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from kmqtAuth.models import KmqtUser, Program
from kmqtAuth.serializers import KmqtUserSerializer, ProgramSerializer, CreateKmqtUserSerializer


class UserPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class ProgramPageNumberPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20


class KmqtUserInfoViewSet(viewsets.ViewSet):
    queryset = KmqtUser.objects.all().order_by('-date_joined')
    http_method_names = ['get']
    pagination_class = UserPageNumberPagination


    def list(self, request, *args, **kwargs):
        user_info = KmqtUser.objects.filter(id=request.user.id) \
            .values('roles', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login')[0]

        role = request.user.roles

        match role:
            case 0:
                user_info['roles'] = ['admin']
            case 1:
                user_info['roles'] = ['user']
            case _:
                user_info['roles'] = ['guest']

        return Response(user_info)


class KmqtUserViewSet(viewsets.ModelViewSet):
    queryset = KmqtUser.objects.all().order_by('-date_joined')
    pagination_class = UserPageNumberPagination
    serializer_class = KmqtUserSerializer
    http_method_names = ['get']

    # get
    def list(self, request, *args, **kwargs):
        # 鉴权
        if request.user.roles != 0:
            self.queryset = self.queryset.filter(~Q(roles=0),
                                                 is_delete__isnull=True)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # post
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # put
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    # patch
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_delete = datetime.now()
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CreateKmqtUserViewSet(viewsets.ModelViewSet):
    queryset = KmqtUser.objects.all()
    serializer_class = CreateKmqtUserSerializer
    http_method_names = ['get', 'post']
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Generate activation url
        instance = KmqtUser.objects.get(username=request.data['username'])
        url = request.build_absolute_uri()
        parsed_url = urlparse(url)
        domain = splitport(parsed_url.netloc)[0]
        activate_url = domain + "/register/user?uuid=" + str(instance.uuid).replace("-", "")
        print(activate_url)

        # 有需要时再启用
        # send_activate_eam_email(request.data['email'], activate_url)

        instance.set_password(request.data['password'])
        instance.save()

        # Clear cache
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = KmqtUser.objects.get(uuid=kwargs['pk'])
        instance.is_activated = True
        instance.save()
        return Response(status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):

        if request.user.roles != 0:
            self.queryset = self.queryset.filter(is_delete__isnull=True)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_delete = datetime.now()
        instance.save()
        # instance.delete()
