from django.shortcuts import render
from accounts.permissions import IsDoctor, IsPatient, IsDoctorOrPatient
from rest_framework.decorators import api_view, permission_classes
from .serializers import ChatIntentSerializer, ChatMessageSerializer
from .models import ChatIntent, ChatMessage
from accounts.models import Doctor, Patient
from api.patient.models import Query
from rest_framework.response import Response
from os import path
import datetime
from .tasks import update_last_message, speech_to_text
from rest_framework import status




@api_view(['POST'])
@permission_classes([IsDoctorOrPatient])
def verify_chat_call(request):
    qid = request.data['qid']
    qtype = request.data['qtype']
    try:
        query = Query.objects.get(id=qid)
        intent = ChatIntent.objects.get(query=query)
        if intent.expired or not intent.active:
           return Response({},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                patient = Patient.objects.get(user=request.user)
                if intent.patient.id != patient.id:
                    return Response({},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({})
            except:
                doctor = Doctor.objects.get(user=request.user)
                if intent.doctor.id != doctor.id:
                    return Response({},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({})
    except:
        return Response({},status=status.HTTP_400_BAD_REQUEST)
    return Response({})



@api_view(['GET'])
@permission_classes([IsDoctorOrPatient])
def get_chatintents(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
        queryset = ChatIntent.objects.all().filter(doctor=doctor,active=True, expired=False)
        serializer = ChatIntentSerializer(queryset, many=True)
        return Response({'chatList': serializer.data})
    except:
        try:
            patient = Patient.objects.get(user=request.user)
            queryset = ChatIntent.objects.all().filter(patient=patient,active=True, expired=False)
            serializer = ChatIntentSerializer(queryset, many=True)
            return Response({'chatList': serializer.data})
        except:
            return Response({'error': 'not allowed'})


from .tasks import update_last_message
@api_view(['POST'])
@permission_classes([IsDoctorOrPatient])
def post_chat(request, query):
    chat_intent = ChatIntent.objects.all().get(query=query)
    if chat_intent is not None:
        if request.data['type'] == 'voice-note':
            chatMessage = ChatMessage(who=request.user, message=None,
                                      voice_note=request.data['messageText'], type=request.data['type'], chat_intent=chat_intent)
            update_last_message.delay(chat_intent.id, 'voice-note',request.user.id,request.data)
            chatMessage.save()
            speech_to_text.delay(chatMessage.id)
        else:
            chatMessage = ChatMessage(who=request.user, voice_note=None,
                                      message=request.data['messageText'], type=request.data['type'], chat_intent=chat_intent)
            update_last_message.delay(chat_intent.id, request.data['messageText'][:50]+'...',request.user.id,request.data)
            chatMessage.save()
        queryset = ChatMessage.objects.all().get(id=chatMessage.id)
        serializer = ChatMessageSerializer(queryset)

        print(chat_intent)
        return Response(serializer.data)
    else:
        return Response({'error': 'access denied'})


@api_view(['GET'])
@permission_classes([IsDoctorOrPatient])
def get_chat(request, query):
    chat_intent = ChatIntent.objects.get(query=query)
    if chat_intent is not None:
        queryset = ChatMessage.objects.all().filter(chat_intent=chat_intent).order_by('time')
        serializer = ChatMessageSerializer(queryset, many=True)
        return Response({'dialog': serializer.data})
