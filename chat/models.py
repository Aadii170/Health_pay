from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# this used to store the group of patient and doctor
class ChatRoom(models.Model):
   group_name = models.CharField(max_length=255)
   

# this is used to store the messages in the specilal chat room
class ChatMessage(models.Model):
    group_name = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)