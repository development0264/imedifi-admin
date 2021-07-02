from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import *
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from accounts.permissions import IsDoctor
from rest_framework import viewsets
from accounts.serializers import SpecialityViewSerializer
from api.patient.models import Query, Feedback
from .serializers import DoctorQueryViewSerializer
from accounts.models import Patient, Doctor, Speciality
from django.views.decorators.csrf import csrf_exempt
from api.chat.tasks import create_chatintent
from django.shortcuts import get_object_or_404



# Create your views here.
@api_view()
@permission_classes([IsDoctor])
def doctor_overview(request):
    return Response({"message": "welcome,doctor "+request.user.email})

class QueryViewSetDoctor(viewsets.ModelViewSet):
    speciality = SpecialityViewSerializer
    queryset = Query.objects.all().order_by('-created')
    serializer_class = DoctorQueryViewSerializer
    permission_classes = [IsDoctor]

    def perform_create(self, serializer):
        pass
    def update(self, requescleart, pk=None):
        pass

    def partial_update(self, request, pk=None):
        if request.GET['a'].strip() == 'leave-feedback':
            doctor = Doctor.objects.get(user=self.request.user)
            queryset = Query.objects.all().filter(doctor=doctor).order_by('-created')
            query = get_object_or_404(queryset, pk=pk)
            if query.is_rated:
               feedback = Feedback.objects.get(query=query)
               feedback.doc_to_pat_rating = request.data['rating']
               feedback.doc_to_pat_feedback = request.data['feedback']
               feedback.save()
            serializer = DoctorQueryViewSerializer(query)
            return Response(serializer.data)
        elif request.GET['a'].strip() == 'send-notes':
            doctor = Doctor.objects.get(user=self.request.user)
            queryset = Query.objects.all().filter(doctor=doctor).order_by('-created')
            query = get_object_or_404(queryset, pk=pk)
            query.notes_from_doctor = request.data['notes']
            query.save()
            serializer = DoctorQueryViewSerializer(query)
            return Response(serializer.data)

    
    

    def list(self, request):
        try:
            doctor = Doctor.objects.get(user_id=self.request.user,is_active=True)
            specs = doctor.specialities.all()
            _specs = [Speciality.objects.get(title='General').id,]
            
            for s in specs:
                _specs.append(s.id)
            print(_specs)
            queryset = Query.objects.all().filter(status='open',active=True,is_archieved=False,doctor=None, speciality__in=_specs).order_by('-created')
            print(queryset)
            serializer = DoctorQueryViewSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response([])

@api_view(['POST'])
@permission_classes([IsDoctor])
@csrf_exempt
def serve(request):
    try:
        qid = request.data['qid']
        query = Query.objects.get(id=qid)
        if query.status == 'open':
            doctor = Doctor.objects.get(user=request.user)
            query.doctor = doctor
            query.status = 'assigned'
            query.save()
            create_chatintent.delay(query.id,doctor.id)
            return Response({'success':True, 'error':False})
        else:
            return Response({'error':True, 'success':False})
    except:
        return Response({'error':True, 'success':False})

@api_view(['GET'])
@permission_classes([IsDoctor])
def my_assigned_queries(request):
        doctor = Doctor.objects.get(user=request.user)
        queryset = Query.objects.all().filter(doctor=doctor)
        serializer = DoctorQueryViewSerializer(queryset, many=True)
        return Response(serializer.data)
   