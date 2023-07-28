from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json
from .models import Chat
from .models import Message


@login_required(login_url='localhost/admin')
def index(request):
    user = request.user
    chat_rooms = Chat.objects.filter(members=user)
    context = {
        "chat_rooms": chat_rooms
    }
    print(context)

    return render(request, "index.html", context)


@login_required(login_url=' admin')
def room(request, room_name):
    username = request.user.username
    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username))
    }
    return render(request, "room.html", context)
