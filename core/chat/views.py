from django.shortcuts import render

from chat.models import *


def index(request):
    chats = Chat.objects.filter(members__in=[request.user])
    messages = TextMessage.objects.filter(chat__in=chats)
    context = {
        'messages': messages,
        'user':  request.user
    }
    return render(request, 'chat/index.html', context)
