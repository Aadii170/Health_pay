from django.contrib import admin
from .models import ChatRoom, ChatMessage
# Register your models here.

admin.site.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('group_name',)


admin.site.register(ChatMessage)    
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'message', 'timestamp')
   
