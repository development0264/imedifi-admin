from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from accounts.permissions import  IsDoctor
from .models import WithdrawlSetting
from rest_framework.response import Response
from accounts.models import Doctor

# Create your views here.


@api_view(['GET','POST'])
@permission_classes([IsDoctor])
def withdrawl_settings(request):
    if request.method == 'POST' and request.data['id']:
        try:
            doctor = Doctor.objects.get(user=request.user)
            try:
                settings = WithdrawlSetting.objects.get(doctor=doctor)
                settings.paypal_id = request.data['id']
                settings.save()
            except:
                settings = WithdrawlSetting(doctor=doctor,paypal_id=request.data['id'])
                settings.save()
            return Response({'success':1})
        except:
            return Response({},status=400)

    elif request.method == 'GET':
        try:
            doctor = Doctor.objects.get(user=request.user)
            settings = WithdrawlSetting.objects.get(doctor=doctor)
            return Response({'paypal_id':settings.paypal_id})
        except:           
            return Response({})
