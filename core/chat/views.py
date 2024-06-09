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

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        message = request.POST.get('message')
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            file_name = default_storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
            file_url = default_storage.url(file_name)
        else:
            file_url = None

        response_data = {
            'message': message,
            'user': user_id,
            'file_url': file_url,
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def test(request):
    return render(request, 'chat/test.html')