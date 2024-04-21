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
    is_active = models.BooleanField(default=True)
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = None
    last_name = None

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
