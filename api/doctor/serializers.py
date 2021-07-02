from rest_framework import serializers
from api.patient.models import Query
from accounts.models import Speciality


class SpecialitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Speciality
    fields = ('title','id',)





class DoctorQueryViewSerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer(read_only=True)
    class Meta:
        model = Query
        fields = ('id','title','present_complaint',
                 'past_history','speciality',
                   'current_medicine','past_medical_history',
                   'past_surgical_history','blood_pressure','temperature','height',
                   'weight','status','query_type','doctor','created','updated','amount','notes_from_doctor'
                 )
