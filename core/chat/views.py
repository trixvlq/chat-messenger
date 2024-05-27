import time

from django.db.models import Subquery, OuterRef
from django.http import JsonResponse
from django.shortcuts import render
from chat.models import *
from chat.serializers import TextMessageSerializer, ChatSerializer


def index(request):
    chats = Chat.objects.filter(members__in=[request.user])
    context = {
        'chats': chats,
        'user': request.user
    }
    return render(request, 'chat/index.html', context)


def chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    messages = TextMessage.objects.filter(chat=chat)
    chat_serializer = ChatSerializer(chat)
    messages_serializer = TextMessageSerializer(messages, many=True)
    context = {
        'chat': chat_serializer.data,
        'messages': messages_serializer.data
    }
    return JsonResponse(context)
