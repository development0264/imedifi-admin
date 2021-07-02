
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from accounts.permissions import *
from django.http.response import  HttpResponseRedirect, HttpResponse



def redirect(request):
    try:
        return HttpResponseRedirect(request.GET['url'].strip())
    except :
        return HttpResponse('error')


@api_view()
@permission_classes([permissions.AllowAny])
def public_api_home(request):
    return Response({"message": "welcome, to api home "})
