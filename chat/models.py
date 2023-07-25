from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)

    def get_last_messages(self):
        last_messages = Message.objects.order_by('-send_time').all()
        return last_messages

    def __str__(self):
        return self.author.username
