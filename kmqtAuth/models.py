import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class KmqtUser(AbstractUser):
    email = models.EmailField(_("email address"))
    role_type = [
        [0, 'admin'],
        [1, 'user'],
    ]
    roles = models.IntegerField(choices=role_type, default=1)
    is_delete = models.DateTimeField(default=None, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = None
    last_name = None

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class DataSet(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)


class Program(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True, null=True)
    author = models.ForeignKey(KmqtUser, on_delete=models.CASCADE)
    is_delete = models.DateTimeField(default=None, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    update_time = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    status_type = [
        [0, 'prepare'],
        [1, 'waiting'],
        [2, 'processing'],
        [3, 'done'],
        [4, 'fail'],
    ]
    status = models.IntegerField(choices=status_type, default=0)
