from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json
from .models import Chat
from .models import Message


@login_required()
def index(request):
    user = request.user
    print(user)
    chat_rooms = Chat.objects.filter(members=user)
    context = {
        "chat_rooms": chat_rooms
    }
    print(context)

    return render(request, "index.html", context)


@login_required()
def room(request, room_name):
    user = request.user
    username = request.user.username
    chat_model = Chat.objects.filter(room_name=room_name)

    if not chat_model.exists():
        Chat.objects.create(room_name=room_name, members=user)
    else:
        print(chat_model[0].members.add(user))

    context = {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username))
    }
    return render(request, "room.html", context)
