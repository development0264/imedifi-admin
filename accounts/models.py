# Create your models here.
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.default_values import  COUNTRIES, ROLES, STATUSES
import random
class Speciality(models.Model): 
    title = models.CharField(_('title'), max_length=256)
    description = models.TextField(_('description'))
    can_subscribed = models.BooleanField(_('can_subscribed'), default=False)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _('speciality')
        verbose_name_plural = _('specialities')


class Country(models.Model):
     name = models.CharField(blank=False, max_length=256)
     code = models.CharField(blank=False, max_length=8)
     class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'
     def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    """custom user manager class"""
    use_in_migration = True
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        try:
            user.first_name = extra_fields.get('name').split(' ')[0]
        except:
            user.first_name = 'n/a'
        try:
            user.last_name = extra_fields.get('name').split(' ')[1]
        except:
            user.last_name = 'n/a'
        
        if user.is_doctor:
            doctor = Doctor(name=user.name,user=user, is_active =False, username=str(round(random.random()*99999999)))
            doctor.save()
        if user.is_patient:
            patient = Patient(name=user.name,user=user)
            patient.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superadmin', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        if extra_fields.get('role') == 'doctor':
            extra_fields.setdefault('is_doctor',True)
            extra_fields.setdefault('is_patient',False)

        elif extra_fields.get('role') == 'patient':
            extra_fields.setdefault('is_patient',True)
            extra_fields.setdefault('is_doctor',False)
        else: 
            return False
        return self._create_user(email, password, **extra_fields)
       

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superadmin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_patient', False)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superadmin') is not True and extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model class"""
    email = models.EmailField(_('email'), unique=True,)
    first_name = models.CharField(_('first_name'), max_length=50, blank=False)
    last_name = models.CharField(_('last_name'), max_length=50, blank=False)
    name = models.CharField(_('name'),max_length=100)
    is_superadmin = models.BooleanField(_('is_superadmin'), default=False)
    is_active = models.BooleanField(_('is_active'), default=False)
    is_patient = models.BooleanField(_('is_patient'), default=False)
    is_doctor = models.BooleanField(_('is_doctor'), default=False)
    is_staff = models.BooleanField(_('is_staff'),default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'dob', 'password', 'phone_number','gender', 'country','role','state']
    objects = CustomUserManager()
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True,null=True)
    dob = models.DateField(_('dob'), blank=False, null=False)
    phone_number = models.CharField(_('phone_number'), max_length=128)
    gender = models.CharField(_('gender'), choices=[('male','male'),('female','female'),('other','other')], max_length=6, default='male')
    country = models.CharField(max_length=32, choices=COUNTRIES)
    profile_img = models.ImageField(_('profile_img'), default="default_profile_img.png")
    role = models.CharField(_('role'), default='patient',max_length=64,choices=ROLES)
    state = models.CharField(_('state'), max_length=128, null=True)
    status = models.CharField(_('status'), default='offline',choices=STATUSES, max_length=64)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """stirng representation"""
        return self.email

class File(models.Model):
    filename = models.FileField(upload_to='files')
    filetype = models.CharField('filetype',max_length=256)

class Certificate(models.Model):
    name = models.CharField(max_length=256, null=False)
    issued_by = models.CharField(max_length=256, null=True)
    license_number = models.CharField(max_length=256, null=False)
    files = models.ForeignKey(File, null=True, on_delete=models.SET_NULL)
    speciality = models.ForeignKey(Speciality,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    qualification = models.CharField(_('qualifications'), max_length=512, default='', blank=True)
    specialities = models.ManyToManyField(Speciality, blank=True, related_name='specialities')
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=256)
    username = models.CharField(max_length=256,unique=True,blank=True)
    certificate = models.ForeignKey(Certificate,on_delete=models.SET_NULL, null=True,default=None,blank=True)

    def __str__(self):
        return self.user.email

class Patient(models.Model):
    name = models.CharField('Patient Name', max_length=256)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email


class Plan(models.Model):
    title = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=512, null=True)
    amount = models.IntegerField(blank=False)
    countries = models.ManyToManyField(Country, blank=True, null=True)
    duration = models.IntegerField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    imedifi_commission = models.FloatField(default=10.0)

    def __str__(self):
        return self.title+ ' - '+self.description

class Customer(models.Model):
    patient  = models.OneToOneField(Patient,null=False, on_delete=models.CASCADE)
    def __str__(self):
        return self.patient.user.email

class UserConfig(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    layout_style = models.CharField(max_length=255, default='layout1')
    config_scroll = models.CharField(max_length=255, default='content')
    
    navbar_display = models.BooleanField(default=True)
    navbar_folded = models.BooleanField(default=True)
    navbar_position = models.CharField(max_length=64, default='left')
    
    footer_display = models.BooleanField(default=True)
    footer_style = models.CharField(default='fixed', max_length=64)
    footer_position = models.CharField(max_length=64, default='below')
    
    toolbar_display = models.BooleanField(default=True)
    toolbar_style = models.CharField(default='fixed', max_length=64)
    toolbar_position = models.CharField(max_length=64, default='below')

    mode = models.CharField(default='fullwidth', max_length=64)
    custom_scrollbars = models.BooleanField(default=True)
    theme_main = models.CharField(default='light1', max_length=64)
    theme_navbar = models.CharField(default='light1', max_length=64)
    theme_toolbar = models.CharField(default='light1', max_length=64)
    theme_footer = models.CharField(default='light1', max_length=64)


    def __str__(self):
        return self.user.email
    class Meta:
        verbose_name = 'userconfig'
        verbose_name_plural = 'userconfigs'

