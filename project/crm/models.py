from django.db import models
from django.conf import settings
import sys
sys.path.append("..")
from accounts.models import User

class Task(models.Model):
    STATUS = {
        (0, "wait"),
        (1, "process"), 
        (2, "done")
    }

    title = models.CharField(max_length=50, blank=False, default="")
    description = models.CharField(max_length=250, default="")
    status = models.IntegerField(choices=STATUS, default=0)
    date_of_create = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now=True)
    data_of_close = models.DateTimeField(auto_now=True)
    report = models.CharField(max_length=250, blank=True)
    customer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks'
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        blank=False,
        default=0
    )