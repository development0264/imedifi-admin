# *.  Payment models (database)
#     this file contains models regarding payment , each payment is mapped to a query


from django.db import models
from accounts.models import Patient, Doctor
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save

from api.patient.models import Query
from .default_values import PLAN_TYPES, QUERY_TYPES


class PaypalToken(models.Model):
    access_token = models.CharField(max_length=4096)
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now=True)

class Payment(models.Model):
    method = models.CharField(max_length=24, choices=(('stripe','stripe'), ('paypal','paypal')))
    amount = models.FloatField()
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=256, null=True, blank=True, default=None)
    paypal_payment_id = models.CharField(max_length=256, null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, choices=(('unpaid','unpaid'),('paid','paid'),('refunded','refunded')))
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    product = models.CharField(max_length=64, choices=QUERY_TYPES)

class Earning(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    query = models.OneToOneField(Query,on_delete=models.CASCADE)
    amount = models.FloatField('amount',default=0)
    status = models.CharField('status',max_length=128,choices=(('pending','pending'),('cleared','cleared'),('dispute','dispute'),('refunded','refunded'),))
    commission_paid = models.FloatField('commision',default=10)
    created = models.DateTimeField('created',auto_now_add=True)
    updated = models.DateTimeField('created',auto_now=True)
