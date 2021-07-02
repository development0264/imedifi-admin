from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from .views import  get_payment_plan,get_user_config, get_specialities, onboarding, upload_file,onboard_doctor,doctor_profile,doctor_my_profile,update_profile_image,get_users_override

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include('djoser.urls')),
    # path('',include('djoser.urls.authtoken')),
    path('', include('djoser.urls.jwt')),
    # path('doctor/login/',obtain_jwt_token),
    path('onboarding/',onboarding),
    path('', include(router.urls)),
    path('plan', get_payment_plan),
    path('uploadFile/', upload_file),
    path('updateProfileImage/', update_profile_image),

    path('onboardDoctor/', onboard_doctor),
    path('drProfile/', doctor_profile),
    path('myDrProfile/', doctor_my_profile),
    path(r'specialities/',get_specialities),
    path('config', get_user_config),
    path('users',get_users_override)





]
