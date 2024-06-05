import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

def upload_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    now = timezone.now()
    return f'{instance.chat.id}/{instance.__class__.__name__.lower()}s/{now.year}/{now.month}/{now.day}/{filename}'


class Chat(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    date_created = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=upload_file, blank=True, null=True)
    image = models.ImageField(upload_to=upload_file, blank=True, null=True)
    video = models.FileField(upload_to=upload_file, blank=True, null=True)
    audio = models.FileField(upload_to=upload_file, blank=True, null=True)

    def read_message(self):
        self.is_read = True
        self.save()

