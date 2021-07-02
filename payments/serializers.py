from rest_framework import serializers
from .models import Payment, Earning
from api.patient.models import Query

class QueryPaymentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Query
      fields = ('id','title', 'status','patient','query_type')

class DoctorEarningSerializer(serializers.ModelSerializer):
   query = QueryPaymentSerializer(read_only=True)
   class Meta:
      model = Earning
      fields = ('id','doctor','query','amount','status','commission_paid','created','updated')


class PaymentViewSerializer(serializers.ModelSerializer):
     query = QueryPaymentSerializer(read_only=True)
     class Meta:
        model = Payment
        fields = ('id','method','amount','query','status','stripe_payment_id','paypal_payment_id','patient','product','updated',)
