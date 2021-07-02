from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SpecialityViewSerializer
from .models import Speciality
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from accounts.permissions import IsPatient, IsDoctorOrPatient, IsAdmin
from .models import Plan
from rest_framework.response import Response
from .serializers import PaymentPlanViewSerializer, DoctorReadSerializer
from accounts.models import Country,UserConfig,User, Doctor, Patient, File, Certificate
from .default_values import DEFAULT_CONFIG
from api.patient.models import Feedback
from api.patient.serializers import PublicFeedbackViewSerializer
import base64


@api_view(['POST'])
@permission_classes([IsDoctorOrPatient])
def update_profile_image(request):
	if request.user and request.data['file']:
	   user = User.objects.get(id=request.user.id)
	   user.profile_img = request.data['file']
	   user.save()
	   return Response({'uploaded':True, 'url':user.profile_img.url})
	return Response({})

@api_view(['GET'])
@permission_classes([AllowAny])
def doctor_my_profile(request):
	doctor = Doctor.objects.get(user=request.user)
	feedbacks = Feedback.objects.all().filter(doctor=doctor)
	serializer = DoctorReadSerializer(doctor)
	feedbacks_serializer = PublicFeedbackViewSerializer(feedbacks, many=True)

	if doctor:
		return Response({'doctor':serializer.data,'feedbacks':feedbacks_serializer.data,})
	else:
		return Response({'doctor':None})

@api_view(['POST'])
@permission_classes([AllowAny])
def doctor_profile(request):
	if request.data['username']:
		print(request.data['username'])
		doctor = Doctor.objects.get(username=request.data['username'])
		feedbacks = Feedback.objects.all().filter(doctor=doctor)
		serializer = DoctorReadSerializer(doctor)
		feedbacks_serializer = PublicFeedbackViewSerializer(feedbacks, many=True)

		if doctor:
			return Response({'doctor':serializer.data,'feedbacks':feedbacks_serializer.data,})
		else:
			return Response({'doctor':None})


@api_view(['GET'])
@permission_classes([IsAdmin])
def get_users_override(request):
	return Response({})

@api_view(['POST'])
@permission_classes([AllowAny])
def onboard_doctor(request):
	cert = request.data['certificate']
	issued_by = request.data['issued_by']
	files = request.data['files']
	speciality = request.data['speciality']
	uid = request.data['uid']
	speciality = Speciality.objects.get(id=speciality)
	user = User.objects.get(id=uid)
	doctor = Doctor.objects.get(user=user)
	username = '{}-doctor-{}-{}'.format(speciality,doctor.user.name,uid)
	doctor.username = username
	doctor.specialities.set([speciality])
	fi = File.objects.all().filter(id__in=files)[0]
	certificate = Certificate(name=cert,issued_by=issued_by,speciality=speciality, files=fi)
	certificate.save()
	doctor.certificate  = certificate
	doctor.save()
	return Response({})


@api_view(['POST'])
@permission_classes([AllowAny])
def upload_file(request):
	if request.data['file']:
	   fi = File(filename=request.data['file'],filetype='nil')
	   fi.save()
	   return Response({'uploaded':True, 'file':fi.id})
	return Response({})


@api_view(['POST'])
@permission_classes([AllowAny])
def onboarding(request):
	uid = request.data['uid']
	token = request.data['token']
	user_id = int(base64.b64decode(uid+'=='))
	user = User.objects.get(id=user_id)
	try:
		doctor = Doctor.objects.get(user=user)
		
		return Response({'utype':user.role,'uid':user.id,'name':user.name,'is_user_active':user.is_active,'is_doctor_active':doctor.is_active})
	except:
		return Response({'utype':user.role,'uid':user.id,'name':user.name,'is_user_active':user.is_active})

@api_view()
@permission_classes([AllowAny])
def get_specialities(request):
	queryset = Speciality.objects.all().order_by('title')
	serializer = SpecialityViewSerializer(queryset,many=True)
	return Response(serializer.data)


@api_view()
@permission_classes([IsPatient])
def get_payment_plan(request):
	country = Country.objects.get(code = request.user.country)
	plan = Plan.objects.all().filter()
	serializer = PaymentPlanViewSerializer(plan,many=True)	
	return Response(serializer.data)
   
@api_view(['GET','POST'])
@permission_classes([IsDoctorOrPatient])
def get_user_config(request):
	if request.method == 'GET':
		try:
			config = UserConfig.objects.get(user=request.user)
		except:
			config = UserConfig(user=request.user)
			config.save()
		conf = {
				'layout': {
					'style': config.layout_style,
					'config': {
						'scroll': config.config_scroll,
						'navbar': {
							'display': config.navbar_display,
							'folded': config.navbar_folded,
							'position': config.navbar_position
						},
						'toolbar': {
							'display': config.toolbar_display,
							'style': config.toolbar_style,
							'position': config.toolbar_position
						},
						'footer': {
							'display': config.footer_display,
							'style': config.footer_style,
							'position': config.footer_position
						},
						'mode': config.mode
					}
				},
				'customScrollbars': config.custom_scrollbars,
				'theme': {
					'main': config.theme_main,
					'navbar': config.theme_navbar,
					'toolbar': config.theme_toolbar,
					'footer': config.theme_footer
				}
			}
		return Response(conf)
	elif request.method == 'POST':
		try:
			config = UserConfig.objects.get(user=request.user)
		except:
			config = UserConfig(user=request.user)
			config.save()
		config.layout_style = request.data['layout']['style']

		config.navbar_display = request.data['layout']['config']['navbar']['display']
		config.navbar_folded = request.data['layout']['config']['navbar']['folded']
		config.navbar_position = request.data['layout']['config']['navbar']['position']

		config.toolbar_display = request.data['layout']['config']['toolbar']['display']
		config.toolbar_style = request.data['layout']['config']['toolbar']['style']
		config.toolbar_position = request.data['layout']['config']['toolbar']['position']

		config.footer_display =request.data['layout']['config']['footer']['display']
		config.footer_style = request.data['layout']['config']['footer']['style']
		config.footer_position = request.data['layout']['config']['footer']['position']
		config.mode = request.data['layout']['config']['mode']

		config.custom_scrollbars = request.data['customScrollbars']
		config.theme_main = request.data['theme']['main']
		config.theme_navbar = request.data['theme']['navbar']
		config.theme_toolbar = request.data['theme']['toolbar']
		config.theme_footer = request.data['theme']['footer']
		config.save()
		return Response({'success':True})