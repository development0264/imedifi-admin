from django.contrib import admin
from .models import ChatIntent,ChatMessage,VoiceMessage

class ChatIntentAdmin(admin.ModelAdmin):
    list_display = ('id','doctor','query','patient','chatType','active','expired','created','updated','expired_at')


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('who','type','time',)



admin.site.register(ChatIntent,ChatIntentAdmin)
admin.site.register(ChatMessage,ChatMessageAdmin)


