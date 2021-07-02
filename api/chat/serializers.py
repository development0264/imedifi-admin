
from rest_framework import serializers
from .models import ChatIntent, ChatMessage
from accounts.models import Doctor, Patient, User


class UserSerializerChat(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('profile_img','name','id')

class DoctorSerializerChat(serializers.ModelSerializer):
    user = UserSerializerChat()
    class Meta:
        model = Doctor
        fields = ('user',)

class PatientSerializerChat(serializers.ModelSerializer):
    user = UserSerializerChat()
    class Meta:
        model = Patient
        fields = ('user',)

class ChatIntentSerializer(serializers.ModelSerializer):
  doctor = DoctorSerializerChat()
  patient = PatientSerializerChat()
  class Meta:
    model = ChatIntent
    fields = ('query','doctor','patient','created','chatType','status','expired','expired_at','active','last_msg')


class ChatMessageSerializer(serializers.ModelSerializer):
    who = UserSerializerChat()
    class Meta:
        model = ChatMessage
        fields = ('who','chat_intent','type','voice_note','message','time',)