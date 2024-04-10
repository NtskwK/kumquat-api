from django.db import models


# Create your models here.
class Equipment(models.Model):
    name = models.CharField(max_length=200)
    program_id = models.IntegerField(blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)
