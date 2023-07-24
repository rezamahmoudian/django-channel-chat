from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)
    

