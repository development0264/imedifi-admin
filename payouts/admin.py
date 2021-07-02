from django.contrib import admin
from .models import WithdrawlSetting


class WithdrawlSettingAdmin(admin.ModelAdmin):
    list_display = ('doctor','paypal_id','created','updated')


admin.site.register(WithdrawlSetting,WithdrawlSettingAdmin)

# Register your models here.
