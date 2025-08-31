from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render
from .models import ChatRoom,ChatMessage # Import your model

# View to render chat interface and pass group name to template
def index(request, group_name):
    # Check if group exists; if not, create it
    group=ChatRoom.objects.filter(group_name=group_name).first()
    msg=[]
    if group:
        msg=ChatMessage.objects.filter(group_name=group)
    else:
        group = ChatRoom(group_name=group_name)
        group.save()

    return render(request, 'chat/index.html', {'group_name': group_name, 'messages': msg})

