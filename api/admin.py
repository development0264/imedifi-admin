from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
     list_display = ('id','who','ntype','title','description','color','visited','ref',)


admin.site.register(Notification,NotificationAdmin)