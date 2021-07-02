
# Register your models here.
from django.contrib import admin
from .models import Payment, Earning, PaypalToken


class EarningAdmin(admin.ModelAdmin):
    list_display = ('doctor','query','amount','status','commission_paid','created','updated')
    list_editable = ('status',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('patient','query','method','amount','status','created','updated')


class PayPalTokenAdmin(admin.ModelAdmin):
    list_display = ('id','access_token','created','updated')
    list_editable = ('access_token',)

admin.site.register(Earning,EarningAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(PaypalToken,PayPalTokenAdmin)

