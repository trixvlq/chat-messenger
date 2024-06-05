import time

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Subquery, OuterRef
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from chat.models import *
from chat.serializers import *


def index(request):
    chats = Chat.objects.filter(members__in=[request.user])
    context = {
        'chats': chats,
        'user': request.user,
    }
    return render(request, 'chat/index.html', context)


def chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)

    messages = ChatMessage.objects.filter(chat=chat).select_related('author').order_by('date_sent')

    messages = ChatMessageSerializer(messages, many=True).data

    chat_serializer = ChatSerializer(chat)

    context = {
        'chat': chat_serializer.data,
        'messages': messages
    }
    print(context)
    return JsonResponse(context)


def dima(request):
    return render(request, 'chat/dima.html')

def test(request):
    return render(request, 'chat/test.html')