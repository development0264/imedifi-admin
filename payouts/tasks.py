from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
import requests
from payments.models import PaypalToken, Earning
from django.utils import timezone
from accounts.models import Plan
from django.utils.translation import ugettext_lazy as _
# from django_celery_beat.models import PeriodicTask, PeriodicTasks
# PeriodicTask.objects.all().update(last_run_at=None)
# for task in PeriodicTask.objects.all():
#     PeriodicTasks.changed(task)



from api.patient.models import Query
from api.chat.models import  ChatIntent
import math


logger = get_task_logger(__name__)

PAYPAL_CLIENT_ID = 'AfNCol6DmZo_XUe_Ecwx-JgnDarv7Ljk7Hp5pQuFFSVCHbjGMA_7lDsglFM0VHvy1uhW-MpFzSMaXt4J'
PAYPAL_SECRET = 'EG--LsgIJFXaqezCyMYGtLeiEtOn8sdPShsos0-xtAQXUZU2mZVhCjgGlH0lKZWICzOfdLT957u5dOH3'
PAYPAL_API_URL = 'https://api-m.sandbox.paypal.com/'


@task(name='refresh_paypal_token')
def refresh_paypal_token():
        res = requests.post(PAYPAL_API_URL+'/v1/oauth2/token',data={'grant_type':'client_credentials'},auth=(PAYPAL_CLIENT_ID,PAYPAL_SECRET),)
        access_token = res.json()['access_token']
        try:
            token = PaypalToken.objects.first()
        except:
            token = PaypalToken(access_token='null')
            token.save()
        token.access_token = access_token
        token.save()
        return True

def pay_paypal(username):
    pass

def close_query(query):
    pass



@task(name='monitor_queries')
def _monitor_queries():
    queryset = Query.objects.all().filter(status='assigned')
    for query in queryset:
        #print(query.status, query.query_type)
        intent = ChatIntent.objects.get(query=query)
        if intent.active:
            if intent.expired_at < timezone.now():
                intent.active = False
                intent.expired = True
                intent.status = 'expired'
                query.active = False
                query.status = 'closed'
                plan = Plan.objects.get(title=query.query_type)
                commission_paid = math.ceil(query.amount * (plan.imedifi_commission/100))
                amount_earned = math.ceil(query.amount-commission_paid)
                earning = Earning(doctor=query.doctor,amount=amount_earned,query=query,status='pending',commission_paid=commission_paid)
                earning.save()
                intent.save()
                query.save()
                continue
    return True

@task(name='release_funds')
def release_funds():
    return 'funds release'
