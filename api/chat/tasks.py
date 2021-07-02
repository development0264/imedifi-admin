
from celery.decorators import task
from .models import ChatIntent, ChatMessage
from accounts.models import Plan
from celery.utils.log import get_task_logger
from time import sleep
import speech_recognition as sr
from api.patient.models import Query
from accounts.models import Doctor
from datetime import datetime, timedelta 
from api.models import Notification
import base64
from pydub import AudioSegment
from io import BytesIO
from django.conf import settings
import uuid
import speech_recognition as sr



logger = get_task_logger(__name__)



@task(name='create_chatintent')
def create_chatintent(qid,doc):
    query = Query.objects.get(id=qid)
    plan  = Plan.objects.get(title=query.query_type)
    _now = datetime.now()
    est_expiry = _now + timedelta(days = plan.duration)
    doctor = Doctor.objects.get(id=doc)
    notification = Notification(ntype='query-assigned',title="Query has been assigned",description="Your query has been assigned to doctor "+query.doctor.user.name,ref=query.id,who=query.patient.user,color='info')
    notification.save()
    intent = ChatIntent(query=query,patient=query.patient,doctor=doctor,status='active',chatType=query.query_type,active=True,expired_at=est_expiry,unread_doctor=1,unread_patient=1)
    intent.save()
    
    


@task(name='update_last_message')
def update_last_message(chat_intent,last_msg,user,data):
    chat_intent = ChatIntent.objects.all().get(id=chat_intent)

    if user==chat_intent.query.patient.user.id:
        who = chat_intent.query.doctor.user
        _from = chat_intent.query.patient.user.name
        chat_intent.unread_doctor = chat_intent.unread_doctor+1
    else:
        who = chat_intent.query.patient.user
        _from = chat_intent.query.doctor.user.name
        chat_intent.unread_patient = chat_intent.unread_patient+1
    if data['isVoiceCall'] or data['isVideoCall']:
        if(data['isVoiceCall']):
           notification = Notification(ntype='call',title="New Call",description="Incoming voice call from "+_from,ref=chat_intent.query.id,who=who,color='success')
           notification.save()
        else:
           notification = Notification(ntype='call',title="New Call",description="Incoming video call from "+_from,ref=chat_intent.query.id,who=who,color='success')
           notification.save()
    else:
        notification = Notification(ntype='chat',title="New Message",description="You recieved a new message from "+_from,ref=chat_intent.query.id,who=who,color='info')
        notification.save()
    
    chat_intent.last_msg = last_msg
    chat_intent.save()

    return('update_last_message done')



NOTES_PATHS = str(settings.BASE_DIR)+'/api/chat/tmp_notes/'
r = sr.Recognizer()


@task(name='speech_to_text')
def speech_to_text(msg):
    chat = ChatMessage.objects.get(id=msg)
    header, body = chat.voice_note.split(',')
    uid = str(uuid.uuid4())
    filename_webm = NOTES_PATHS+uid+'.webm'
    filename_wav = NOTES_PATHS+uid+'.wav'
    decoded = base64.b64decode(body)
    with open(filename_webm,'wb') as tmpWebmFile:
        tmpWebmFile.write(decoded)
    
    sound = AudioSegment.from_file(filename_webm, format = 'webm')
    sound.export(filename_wav, format="wav")

    with sr.AudioFile(filename_wav) as source:
        audio = r.record(source)
        try:
            text =  r.recognize_google(audio)
            chat.message = text;
            chat.save()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return('voice_recognized done')

