from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


# Create your models here.
class Member(AbstractUser):
    role_type = [
        [0, 'admin'],
        [1, 'user'],
    ]

    roles = models.IntegerField(choices=role_type, default=1)
    name = models.CharField(max_length=150)
    is_delete = models.DateTimeField(default=None, blank=True, null=True)


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
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_delete = models.DateTimeField(default=None, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    status_type = [
        [0, 'prepare'],
        [1, 'waiting'],
        [2, 'processing'],
        [3, 'done'],
        [4, 'fail'],
    ]
    status = models.IntegerField(choices=status_type, default=0)
