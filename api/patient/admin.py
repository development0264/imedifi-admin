from django.contrib import admin
from api.patient.models import Query, QueryDoc, Feedback
from django.urls import reverse
from django.utils.html import format_html


# Register your models here.

class QueryAdmin(admin.ModelAdmin):
    list_display = ('title','speciality','status','doctor','active','amount','created','updated',)

class QueryDocAdmin(admin.ModelAdmin):
    def query_link(self, obj):
        link = reverse("admin:patient_query_change", args=[obj.query.id])
        return format_html('<a href="{}">{}</a>',link,obj.query.title)

    list_display = ('id','query_link','src','created',)

admin.site.register(Query,QueryAdmin)
admin.site.register(QueryDoc,QueryDocAdmin)
admin.site.register(Feedback)


