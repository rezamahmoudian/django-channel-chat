from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user = get_user_model()


class Chat(models.Model):
    roomname = models.CharField(max_length=100)
    members = models.ManyToManyField(user, null=True, blank=True)

    def __str__(self):
        return self.roomname


class Message(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()
    related_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True, null=True)
    send_time = models.DateTimeField(auto_now_add=True)

    def get_last_messages(self, roomname):
        last_messages = Message.objects.filter(related_chat__roomname=roomname).order_by('-send_time')
        return last_messages

    def __str__(self):
        return self.author.username
