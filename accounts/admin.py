# from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.contrib import admin
from .models import User, Doctor, Certificate, Patient, Speciality, Country, Plan, UserConfig, File
from django.urls import reverse
from django.utils.html import format_html

class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','dob','gender','country','is_doctor','is_patient',)
    list_filter = ('gender','country',)

class DoctorAdmin(admin.ModelAdmin):
    def certificate_link(self, obj):
        if obj.certificate:
            link = reverse("admin:accounts_certificate_change", args=[obj.certificate.id])
            return format_html('<a href="{}">{}</a>',link,obj.certificate.id)
        else:
            return format_html('<a href="#">{}</a>','None')

    list_display = ('id','username','name','user','certificate_link','is_active','qualification')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('name','user',)

class CertificateAdmin(admin.ModelAdmin):
    def files_link(self, obj):
        #link = reverse("admin:accounts_file_change", args=[obj.files.id])
        return format_html('<a href="{}">{}</a>',f'/media/{obj.files.filename}',obj.files.filename)
    list_display = ('name','issued_by','speciality','files_link')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name','code',)

class FileAdmin(admin.ModelAdmin):
    list_display = ('id','filename','filetype',)

class PlanAdmin(admin.ModelAdmin):
    list_display = ('title','description','amount','duration','imedifi_commission',)


class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('title','description','can_subscribed',)

admin.site.register(User, UserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Patient,PatientAdmin)
admin.site.register(Speciality,SpecialityAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(Plan,PlanAdmin)
admin.site.register(UserConfig)
admin.site.register(File,FileAdmin)
admin.site.site_header = "Imedifi Admin"
admin.site.site_title = "Imedifi Admin Portal"
admin.site.index_title = "Welcome to Imedifi Admin Portal"