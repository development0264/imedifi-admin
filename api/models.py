from accounts.models import Doctor, Patient, User
from django.db import models
from api.patient.models import Query

class Notification(models.Model):
    ntype = models.CharField('type', max_length=64, choices=(('chat','chat'),('call','call'),
                                                        ('query-assigned','query-assigned'),
                                                        ('query-expired','query-expired'),
                                                        ('admin','admin'),('system','system'),))
    title = models.CharField('title', max_length=2048)
    description = models.CharField('description',max_length=4096)
    color = models.CharField('color',max_length=64,choices=(('info','info'),('success','success'),
                                                            ('error','error'),('warning','warning'),
                                                            ('primary','primary'),('secondary','secondary'),))
    visited = models.BooleanField('is_visited', default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ref = models.CharField('ref', max_length=256)
    who = models.ForeignKey(User, on_delete=models.CASCADE)

class Rating(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    feedback = models.CharField('feedback', max_length=1050)
    query = models.OneToOneField(Query, on_delete=models.CASCADE)

# class Message(models.Model):
#     msg_type = models.CharField('type', max_length=256, choices=((0, 'text'), (1, 'file'), (2, 'text_file')))
#     body =  models.CharField('body', max_length=2048)

# class FreeQuery(models.Model):
#     text_queries = models.SmallIntegerField(default=0)
#     voice_queries = models.SmallIntegerField(default=0)
#     video_queries = models.SmallIntegerField(default=0)
#     text_queries = models.SmallIntegerField(default=0)


