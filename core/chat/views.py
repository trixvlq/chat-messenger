import time

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Subquery, OuterRef
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat.models import *
from chat.serializers import *


def index(request):
    chats = Chat.objects.filter(members__in=[request.user])
    context = {
        'chats': chats,
        'user': request.user
    }
    return render(request, 'chat/index.html', context)


def chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    texts = TextMessage.objects.filter(chat=chat_id)
    images = ImageMessage.objects.filter(chat=chat_id)
    files = FileMessage.objects.filter(chat=chat_id)
    videos = VideoMessage.objects.filter(chat=chat_id)
    audios = AudioMessage.objects.filter(chat=chat_id)
    stickers = StickerMessage.objects.filter(chat=chat_id)

    result = []

    for i in texts:
        result.append(TextMessageSerializer(i).data)
    for i in images:
        result.append(ImageMessageSerializer(i).data)
    for i in files:
        result.append(FileMessageSerializer(i).data)
    for i in videos:
        result.append(VideoMessageSerializer(i).data)
    for i in audios:
        result.append(AudioMessageSerializer(i).data)
    for i in stickers:
        result.append(StickerMessageSerializer(i).data)

    result.sort(key=lambda x: x['date_sent'])

    chat_serializer = ChatSerializer(chat)

    context = {
        'chat': chat_serializer.data,
        'messages': result
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