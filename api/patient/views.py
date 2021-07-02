from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import *
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from accounts.permissions import IsPatient
from accounts.models import Doctor, Patient, Speciality, Plan
from rest_framework import generics
from accounts.serializers import DoctorReadSerializer
from rest_framework import viewsets
from .models import Query, Feedback
from .serializers import PatientQueryViewSerializer,PatientQueryCreateSerializer, PatientFeedbackViewSerializer, QueryDocSerializer
from accounts.serializers import SpecialityViewSerializer
from accounts.models import Plan
from django.shortcuts import get_object_or_404
from api.chat.models import ChatIntent
from django.db.models import Q
import math
from payments.models import Earning
from .models import  QueryDoc

# Create your views here.


@api_view(['GET'])
@permission_classes([IsDoctorOrPatient])
def fetch_query_file(request, qid):
    try:
        query = Query.objects.get(id=qid)
        queryset = QueryDoc.objects.filter(query=query)
        serializer = QueryDocSerializer(queryset,many=True)
        return Response(serializer.data)
    except:
        return Response([])


@api_view(['POST'])
@permission_classes([IsDoctorOrPatient])
def upload_query_file(request, qid):
    try:
        query = Query.objects.get(id=qid)
        qdoc = QueryDoc(src = request.data['file'], query=query)
        qdoc.save()
        serializer = QueryDocSerializer(qdoc)
        return Response(serializer.data)
    except:
        pass

@api_view()
@permission_classes([IsPatient])
def patient_overview(request):
    return Response({"message": "welcome, patient "+request.user.email})

@api_view()
@permission_classes([IsDoctorOrPatient])
def get_query_feedback(request,qid):
    try:
        patient = Patient.objects.get(user=request.user)
        queryset = Feedback.objects.all().filter(patient=patient,query=qid)
        feedback = get_object_or_404(queryset, query=qid)
        serializer = PatientFeedbackViewSerializer(feedback)        
        return Response(serializer.data)
    except Patient.DoesNotExist:
        doctor = Doctor.objects.get(user=request.user)
        queryset = Feedback.objects.all().filter(doctor=doctor,query=qid)
        feedback = get_object_or_404(queryset, query=qid)
        serializer = PatientFeedbackViewSerializer(feedback)        
        return Response(serializer.data)
        





class QueryViewSet(viewsets.ModelViewSet):
    speciality = SpecialityViewSerializer
    queryset = Query.objects.all().order_by('-created')
    serializer_class = PatientQueryCreateSerializer
    permission_classes = [IsDoctorOrPatient]


    def list(self, request):
        patient = Patient.objects.get(user_id=self.request.user)
        queryset = Query.objects.all().filter(patient=patient).order_by('-created')
        serializer = PatientQueryViewSerializer(queryset, many=True)
        return Response(serializer.data)

    
    def retrieve(self, request, pk=None):
        try:
            patient = Patient.objects.get(user_id=self.request.user)
            queryset = Query.objects.all().filter(patient=patient)
            query = get_object_or_404(queryset, pk=pk)
            serializer = PatientQueryViewSerializer(query)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            doctor = Doctor.objects.get(user_id=self.request.user)
            specs = doctor.specialities.all()
            _specs = [Speciality.objects.get(title='General').id,]
            for s in specs:
             _specs.append(s.id)

            queryset = Query.objects.all().filter(Q(doctor=doctor) | Q(status=open) | Q(speciality__in=_specs))
            query = get_object_or_404(queryset, pk=pk)
            serializer = PatientQueryViewSerializer(query)
            return Response(serializer.data)



    def perform_create(self, serializer):
        patient = Patient.objects.get(user_id=self.request.user)
        serializer.save(patient=patient)

    def update(self, requescleart, pk=None):
        patient = Patient.objects.get(user_id=self.request.user)
        queryset = Query.objects.all().filter(patient=patient).order_by('-created')
        query = get_object_or_404(queryset, pk=pk)
        serializer = PatientQueryViewSerializer(query)
        return Response(serializer.data)

    
    def partial_update(self, request, pk=None):
        if request.GET['a'].strip() == 'update-status':
            patient = Patient.objects.get(user_id=self.request.user)
            queryset = Query.objects.all().filter(patient=patient).order_by('-created')
            query = get_object_or_404(queryset, pk=pk)
            if query.status == 'assigned' and request.data['status'].strip()=='closed':
                query.status = 'closed'
                query.active = False
                chat_intent = ChatIntent.objects.get(query=query)
                chat_intent.active = False
                chat_intent.expired = True
                chat_intent.save()
                query.save()
                plan = Plan.objects.get(title=query.query_type)
                commission_paid = math.ceil(query.amount * (plan.imedifi_commission/100))
                amount_earned = math.ceil(query.amount-commission_paid)

                earning = Earning(doctor=query.doctor,amount=amount_earned,query=query,status='pending',commission_paid=commission_paid)
                earning.save()
                serializer = PatientQueryViewSerializer(query)
                return Response(serializer.data)

        elif request.GET['a'].strip() == 'leave-feedback':
            patient = Patient.objects.get(user_id=self.request.user)
            queryset = Query.objects.all().filter(patient=patient).order_by('-created')
            query = get_object_or_404(queryset, pk=pk)
            if not query.is_rated:
               feedback = Feedback(query=query,pat_to_doc_rating=request.data['rating'], pat_to_doc_feedback=request.data['feedback'],patient=query.patient,doctor=query.doctor)
               query.is_rated = True
               query.save()
               feedback.save()
            
            serializer = PatientQueryViewSerializer(query)
            print('leaving the feedback')
            return Response(serializer.data)
