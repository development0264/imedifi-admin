from django.urls import path,include
from api.views import overview
from payments.views import create_session, session_failed, session_success, hook, PaymentViewSet, DoctorEarningList, paypal_success
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'history', PaymentViewSet,)

urlpatterns = [
    # path('stripe/', checkout),
     path('stripe/createSession/',create_session),
     path('stripe/success/',session_success),
     path('stripe/failed/<pid>/',session_failed),
     path('stripe/webhook/',hook),
     path('myEarnings/', DoctorEarningList.as_view()),
     path('paypal/success/',paypal_success),
     path('',include(router.urls)),

]