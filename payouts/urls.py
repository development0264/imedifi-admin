
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import withdrawl_settings


urlpatterns = [
    path('settings/',withdrawl_settings),
]


