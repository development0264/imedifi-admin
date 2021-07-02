from django.db import models
from accounts.models import Doctor
# Create your models here.


class WithdrawlSetting(models.Model):
    doctor = models.OneToOneField(Doctor,on_delete=models.SET_NULL,null=True)
    paypal_id = models.CharField('paypal id', max_length=512)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


