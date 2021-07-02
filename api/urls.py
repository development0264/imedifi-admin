from django.urls import path,include
from api.views import overview, guest_overview, notifications_get

urlpatterns = [
    path('doctor/', include('api.doctor.urls') ),
    path('patient/', include('api.patient.urls') ),
    path('chat/', include('api.chat.urls')),
    path('notifications/',notifications_get)
]