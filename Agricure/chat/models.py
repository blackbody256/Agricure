from django.db import models
from users.models import User

class ChatSession(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats', default=1)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats', default=1)
    last_updated = models.DateTimeField(auto_now=True)

class Message(models.Model):
    chat = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    # models.py
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
