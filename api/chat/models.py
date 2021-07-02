from django.db import models
from api.patient.models import Query
from accounts.models import Doctor, Patient, User

# Create your models here.
class ChatIntent(models.Model):
    query = models.OneToOneField(Query, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    last_msg = models.CharField(max_length=255, blank=True, null=True)
    chatType = models.CharField(max_length=32, choices=(('text-note','text-note'),('voice-note','voice-note'),
                                                        ('voice-call','voice-call'),('video-call','video-call'),))
    status = models.CharField(max_length=24, choices=(('active','active'), ('expired','expired')))
    
    expired_at = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    unread_patient = models.IntegerField(default=0)
    unread_doctor = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    expired = models.BooleanField(default=False)
    def __str__(self):
        return "doctor: {},patient: {},chatType: {}, status: {}, active: {}".format(self.doctor,self.patient,self.chatType,self.status,self.active)



class ChatMessage(models.Model):
    chat_intent = models.ForeignKey(ChatIntent,on_delete=models.CASCADE)
    who = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=24, choices=(('text-note','text-note'),('voice-note','voice-note')), default='text-note')
    voice_note = models.CharField(max_length=10485759, null=True)
    message = models.CharField(max_length=12000, null=True)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
         return "message: {},who: {},chat_intent: {}".format(self.message,self.who,self.chat_intent)



class VoiceMessage(models.Model):
    chat_intent = models.ForeignKey(ChatIntent,on_delete=models.CASCADE)
    who = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=4000096)
    time = models.DateTimeField(auto_now_add=True)
