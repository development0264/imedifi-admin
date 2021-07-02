from rest_framework import serializers
from .models import Query, Feedback, QueryDoc
from accounts.models import Doctor , User, Speciality, Patient


class QueryDocSerializer(serializers.ModelSerializer):
  class  Meta:
    model = QueryDoc
    fields = ('id','src',)

class DoctorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Doctor
    fields = ('name','username',)

class FeedbackUserSerializer(serializers.ModelSerializer):
  class Meta:
     model = User
     fields = ('name','profile_img',)


class PatientSerializer(serializers.ModelSerializer):
  user = FeedbackUserSerializer(read_only=True)
  class Meta:
    model = Patient
    fields = ('name','user',)

class SpecialitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Speciality
    fields = ('title','id',)
    


class PatientFeedbackViewSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = ('query','doc_to_pat_rating','pat_to_doc_rating',
                 'doc_to_pat_feedback','pat_to_doc_feedback','doctor',
                   'patient','created',
                   'updated',
                 )
class PublicQuerySerializer(serializers.ModelSerializer):
      speciality = SpecialitySerializer(read_only=True)
      patient = PatientSerializer(read_only=True)
      class Meta:
          model = Query
          fields = ('title','speciality','patient')

class PublicFeedbackViewSerializer(serializers.ModelSerializer):
    query = PublicQuerySerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = ('query','doc_to_pat_rating','pat_to_doc_rating',
                 'doc_to_pat_feedback','pat_to_doc_feedback','created',
                 )



class PatientQueryViewSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    speciality = SpecialitySerializer(read_only=True)
    class Meta:
        model = Query
        fields = ('id','title','present_complaint',
                 'speciality','past_history','amount',
                   'current_medicine','past_medical_history',
                   'past_surgical_history','blood_pressure','temperature','height',
                   'weight','status','active','query_type','doctor','created','updated','is_rated','notes_from_doctor',
                 )

class PatientQueryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ('id','title','present_complaint',
                 'speciality','past_history','amount',
                   'current_medicine','past_medical_history',
                   'past_surgical_history','blood_pressure','temperature','height',
                   'weight','status','active','query_type','created','updated',
                 )


