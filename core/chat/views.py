import os
import re

from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.db.models import Subquery, OuterRef
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from chat.models import *
from chat.serializers import ChatMessageSerializer, ChatSerializer


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


def test(request):
    chats = Chat.objects.filter(members__in=[request.user])
    context = {
        'chats': chats,
        'user': request.user,
    }
    return render(request, 'chat/test.html', context)


def sanitize_filename(filename):
    filename = filename.replace(' ', '_')
    filename = ''.join(c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in filename)
    return filename


@csrf_exempt
def upload_file(request, chat_id):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        now = timezone.now()

        file_extension = os.path.splitext(file.name)[1]

        unique_filename = f'{uuid.uuid4().hex}{file_extension}'

        sanitized_filename = sanitize_filename(file.name)
        sanitized_filename_with_extension = f'{unique_filename}'

        file_path = os.path.join(f'{chat_id}/{now.year}/{now.month}/{now.day}', sanitized_filename_with_extension)

        filename = fs.save(file_path, file)
        file_url = fs.url(filename)

        return JsonResponse({'success': True, 'file_url': file_url})
    return JsonResponse({'success': False, 'error': 'File upload failed'}, status=400)


def login_view(request):
    return render(request, 'registration/login.html')


def register_view(request):
    return render(request, 'registration/register.html')
