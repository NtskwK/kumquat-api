import uuid

from django.db import models

from kmqtAuth.models import KmqtUser


# Create your models here.
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
