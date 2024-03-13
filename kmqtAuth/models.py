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
    is_delete = models.BooleanField(default=False)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
