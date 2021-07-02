from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from accounts.models import *


class SpecialityViewSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = Speciality
        fields = ('title','id')

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','email','first_name','last_name','phone_number', 'country','role','profile_img')


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id','email','name','first_name','last_name','phone_number', 'country','profile_img', 'role', 'status')

class CurrentUserDoctorSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('name', 'country','profile_img', 'status','gender',)



class DoctorCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ('name','issued_by',)

class DoctorReadSerializer(serializers.Serializer):
   specialities = SpecialityViewSerializer(read_only=True,many=True)
   user  = CurrentUserDoctorSerializer(read_only=True)
   certificate = DoctorCertificateSerializer(read_only=True)
   class Meta:
        model = Doctor
        fields = ('username','user','specialities','certificate','user.gender',)



class PaymentPlanViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('title','description',
                 'amount','countries','duration'
                   )
