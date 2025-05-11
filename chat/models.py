from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ChatUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_new_message = models.BooleanField(default=False)
    pfp = models.ImageField(upload_to='pfp/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Support(models.Model):
    name = models.CharField(max_length=200)
    pfp = models.ImageField(upload_to='support_pfp')

    def __str__(self):
        return f'Customer support {self.name}'

class Chat(models.Model):
    chat_id = models.CharField(max_length=20)
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    support = models.ForeignKey(Support, on_delete=models.PROTECT)
    last_message = models.TextField(blank=True, null=True)
    last_edited = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=True)

    def __str__(self):
        return f'Chat between support and {self.user.user.username}'
    


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='messages', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    from_support = models.BooleanField(default=False)





