from django.db import models
from accounts.models import Speciality, Patient, Doctor
from .default_values import QUERY_TYPES, QUERY_STATUS_TYPES
# Create your models here.



class Query(models.Model):
    title  = models.CharField('title', max_length=1024)
    present_complaint = models.CharField('present_complaint', max_length=4048)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    past_history = models.CharField('past_history',blank=True, max_length=4048)
    current_medicine  = models.CharField('current_medicine',blank=True, max_length=1024)
    past_medical_history = models.CharField('past_medical_history',blank=True, max_length=4048)
    past_surgical_history = models.CharField('past_surgical_history',blank=True, max_length=4048)
    blood_pressure = models.CharField('blood_pressure',blank=True, max_length=256)
    temperature = models.CharField('temperature',blank=True, max_length=256)
    height = models.CharField('height', blank=True,max_length=256)
    weight = models.CharField('weight', blank=True, max_length=256)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True, default=None)
    status = models.CharField(max_length=128, default='unpaid', choices=QUERY_STATUS_TYPES)
    is_archieved = models.BooleanField(default=False)
    is_rated = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    query_type = models.CharField(blank=False, max_length=48, choices=QUERY_TYPES)
    notes_from_doctor = models.TextField(blank=True,default=None,null=True)
    amount = models.FloatField()


    
    class Meta:
        verbose_name = 'query'
        verbose_name_plural = 'queries'

    def __str__(self):
        """stirng representation"""
        return "{},status: {},patient: {} ".format(self.title,self.status,self.patient)


class Feedback(models.Model):
    query = models.OneToOneField(Query,on_delete=models.CASCADE)
    doc_to_pat_rating = models.IntegerField('Doctor to patient rating',default=0)
    pat_to_doc_rating = models.IntegerField('Patient to doctor rating',default=0)
    doc_to_pat_feedback = models.CharField('Doctor to patient feedback',max_length=4000)
    pat_to_doc_feedback = models.CharField('Patient to doctor feedback',max_length=4000)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class QueryDoc(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    src = models.FileField(upload_to='queries', null=False)
    created = models.DateTimeField(auto_now_add=True)
    

