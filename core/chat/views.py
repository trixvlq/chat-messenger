import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from chat.forms import UserRegisterForm
from chat.models import *
from chat.serializers import ChatMessageSerializer, ChatSerializer, UserSerializer


def chat(request, chat_id):
    chat = Chat.objects.get(id=chat_id)

    messages = ChatMessage.objects.filter(chat=chat).select_related('author').order_by('date_sent')

    messages = ChatMessageSerializer(messages, many=True).data

    chat_serializer = ChatSerializer(chat)

    other_user = chat.members.exclude(id=request.user.id).first()
    if other_user:
        other_user_serializer = UserSerializer(other_user)
    else:
        other_user_serializer = None

    context = {
        'chat': chat_serializer.data,
        'messages': messages,
        'other_user': other_user_serializer.data
    }
    print(context)
    return JsonResponse(context)


def user_info(request, user_id):
    user = get_object_or_404(ChatUser, id=user_id)
    context = {
        'user': user
    }
    return JsonResponse(context)


def test(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
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


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.name = request.POST['name']
            user.surname = request.POST['surname']
            user.nickname = request.POST['nickname']
            print(user)
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, form.errors)
            return render(request, 'registration/sign_up.html', {'form': form})
    form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'registration/sign_up.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            user = ChatUser.objects.get(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
            messages.error(request, 'Wrong username or password')
            return render(request, 'registration/sign_in.html')
    return render(request, 'registration/sign_in.html')


def change_credentials(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.save()
        return redirect('main')


def find_user_by_any_data(data):
    user = ChatUser.objects.get(Q(nickname=data) | Q(username=data) | Q(name=data))
    return user


def search(request):
    if request.method == "POST":
        result = request.POST['search']
        user = find_user_by_any_data(result)
        if user and user!=request.user:
            chat,created = Chat.objects.get_or_create(
                name=f'{user.username} - {request.user.username}',
            )
            if created:
                chat.members.add(request.user,user)
                usernames = '-'.join(str(member.id) for member in chat.members.all())
                chat.room_name = usernames
                if Chat.objects.filter(room_name=chat.room_name).exists():
                    messages.error(request, 'Chat already exists')
                    return redirect('main')
                chat.save()
            else:
                messages.error(request, 'Chat already exists')
        return redirect('main')


def logout_view(request):
    logout(request)
    return redirect('main')

