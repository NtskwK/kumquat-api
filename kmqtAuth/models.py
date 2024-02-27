from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Member(AbstractUser):
    role_type = [
        [0, 'admin'],
        [1, 'user'],
    ]

    roles = models.IntegerField(choices=role_type, default=1)
    name = models.CharField(max_length=150)
    last_login = models.DateTimeField(_('last login'), auto_now=True, blank=True, null=True)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
