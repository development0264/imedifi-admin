from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework import permissions
import stripe
from django.views.decorators.csrf import csrf_exempt
from .models import Payment, Earning, PaypalToken
from accounts.models import Patient, Doctor
from api.patient.models import Query
from accounts.permissions import IsPatient, IsDoctor
from rest_framework import viewsets, generics
from .serializers import PaymentViewSerializer, DoctorEarningSerializer
from django.shortcuts import get_object_or_404
import requests
from django.conf import settings

# def checkout(request):
# 	if request.user.is_authenticated:
# 		cart = Customer.objects.get(user= request.user).cart
# 		total = cart.aggregate(Sum('product_price'))['product_price__sum']
# 		return render(request,"main/checkout.html", {"cart":cart, "total":total})
# 	else:
# 		redirect("main:homepage")
stripe.api_key = 'sk_test_51HN0hxDzOwLWNTSz5LFdvJ9TRF65F01OXYhbUa1n7qvQ1Xf9Pgs3dY3NjlO77TpBsutDdHiFiqkiJ4XUrT2yB4pi008Qf0gXza'


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentViewSerializer
    permission_classes = [IsPatient]
    queryset = Payment.objects.all().order_by('-created')

    def list(self, request):
      permission_classes = [IsPatient]
      patient = Patient.objects.get(user=request.user)
      queryset = Payment.objects.all().filter(patient=patient).order_by('-created')
      serializer = PaymentViewSerializer(queryset,many=True)
      return Response(serializer.data)


    def retrieve(self, request, pk=None):
        query = get_object_or_404(queryset, pk=pk)
        serializer = PaymentViewSerializer(query)
        permission_classes = [IsPatient]
        return Response(serializer.data)

class DoctorEarningList(generics.ListAPIView):
    serializer_class = DoctorEarningSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        doctor = Doctor.objects.get(user=self.request.user)
        return Earning.objects.filter(doctor=doctor)



@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def create_session(request):
    amount = request.data['amount']
    product = request.data['product']
    query = Query.objects.all().filter(id=request.data['query']).first()

    patient = Patient.objects.filter(user=request.user).first()
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    customer_email = request.user.email,
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': product,
        },
        'unit_amount': amount,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url=settings.FRONTEND_URL+'/patient/queries/'+str(query.id)+'?success=true',
    cancel_url=settings.FRONTEND_URL+'/patient/queries/'+str(query.id)+'?success=false',
      )

    
    payment = Payment(patient=patient, method='stripe',amount=amount/100
                    ,query=query,stripe_payment_id=session["payment_intent"],product=product, status='unpaid')
    payment.save()
    return Response(session)


PAYPAL_API_URL = 'https://api-m.sandbox.paypal.com/'

@api_view(['POST','GET'])
@permission_classes([permissions.AllowAny])
def paypal_success(request):
   token = PaypalToken.objects.first()
   if token and request.data['data']['orderID'] and request.data['query']: 
      res = requests.get(PAYPAL_API_URL
      +'/v2/checkout/orders/'+request.data['data']['orderID'].strip(),headers={'Authorization':'Bearer '+token.access_token})
      order = res.json()
      if order and order['status'] == 'COMPLETED':
         paypal_order_id = order['id']
         amount = float(order['purchase_units'][0]['amount']['value'])
         payer_id = order['payer']['payer_id']
         patient = Patient.objects.get(user=request.user)
         query = Query.objects.get(id=request.data['query'])
         payment = Payment(patient=patient, method='paypal',amount=amount
                    ,query=query,paypal_payment_id=paypal_order_id,product=query.query_type, status='paid')
         query.active = True
         query.status = 'open'
         query.save()
         payment.save()
         return Response({'status': 'payment_success'})
      else:
         return Response({'error': 'paypal validation error'})
   else:
      return Response({'error': 'incomplete params provided'})


  


    # print(request.headers)


   return Response({'status': 'payment_success'})




@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def session_success(request):
    print(request.headers)
    return Response({'status': 'payment_success'})


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def session_failed(request, pid):
    print(request)
    return Response({'status': 'payment_failed', 'pid': pid})
    

from django.http import HttpResponse



def stripe_webhook(request):
  print(request)
  return HttpResponse('ok')

@csrf_exempt
def hook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None
  endpoint_secret = 'whsec_kPUle4OvhZFtT2kbSZDzzV17Gb2Dmypn'

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    payment_intent = session['payment_intent']
    payment = Payment.objects.all().filter(stripe_payment_id=payment_intent).first()
    payment.status = 'paid'
    query = Query.objects.get(id=payment.query.id)
    query.status = 'open'
    query.active = True
    query.is_archieved = False
    query.save()
    payment.save()
  return HttpResponse('ok')