from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from .models import Category,Blog
from rest_framework.decorators import api_view,permission_classes,authentication_classes,action
from rest_framework.permissions import AllowAny
from django.core import serializers
from .serializers import BlogSerializer, SerializerBlog
from rest_framework.response import Response
# Create your views here.

@authentication_classes([])
@permission_classes([])
class DisplayCatogery(APIView):
    def get(self,request):
        data = Category.objects.all().values()
        return Response(data)

@authentication_classes([])
@permission_classes([])
class GetCatDetails(APIView):
    def post(self,request):
        id= request.data['id']
        data = Blog.objects.values().filter(category=id)
        return Response(data)

def Get_all_blogs(request, pid):
    data = Blog.objects.filter(category__pk=pid)
    serializer = SerializerBlog(data, many=True)
    print(serializer.data)
    return JsonResponse(serializer.data,safe=False)


def Get_all_cat(request, pid):
    data = Category.objects.filter(id=pid)
    serializer = BlogSerializer(data, many=True)
    print(serializer.data)
    return JsonResponse(serializer.data,safe=False)