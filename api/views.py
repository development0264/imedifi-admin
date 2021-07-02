from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from accounts.permissions import *
from .models import Notification
from .serializers import NotificationSerializer
from .tasks import read_notifications


@api_view()
@permission_classes([IsAuthenticated])
def overview(request):
    return Response({"message": "welcome, "+request.user.email})

@api_view()
@permission_classes([IsAuthenticated])
def notifications_get(request):
    notis = Notification.objects.all().filter(who=request.user,visited=False)
    serializer =NotificationSerializer(notis,many=True)
    print(serializer.data)
    if serializer.data:
        read_notifications.delay(serializer.data)
    return Response(serializer.data)
    


@api_view()
@permission_classes([permissions.AllowAny])
def guest_overview(request):
    return Response({"message": "welcome, Guest "})

