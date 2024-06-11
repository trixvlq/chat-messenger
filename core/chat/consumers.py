from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import *
from .serializers import *


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_author(self, user_id):
        return ChatUser.objects.get(id=user_id)

    @database_sync_to_async
    def get_chat(self, chat_id=1):
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def get_messages(self, chat_id):
        messages = ChatMessage.objects.filter(chat=chat_id)
        return ChatMessageSerializer(messages, many=True).data

    # Фабричный метод инкапсулирующий создание объектов

    @database_sync_to_async
    def create_message(self, chat, user, message, file):
        return ChatMessage.objects.create(
            chat=chat,
            author=user,
            content=message,
            file=file
        )

    @database_sync_to_async
    def if_user_in_chat(self, user, chat):
        return user in chat.members.all()

    @database_sync_to_async
    def get_user(self, user_id):
        return ChatUser.objects.get(id=user_id)

    @database_sync_to_async
    def read_message(self, message):
        message = ChatMessage.objects.get(id=message)
        if message.is_read == False and message.author != self.user:
            message.is_read = True
            message.save()

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            print('yep')
            self.chat = await self.get_chat(self.chat_id)
            self.room_group_name = f'chat_{self.chat_id}'

            if not self.chat:
                await self.send(text_data=json.dumps({'error': 'Chat does not exist'}))
                await self.close()
                return

            if not await self.if_user_in_chat(self.user, self.chat):
                await self.send(text_data=json.dumps({'error': 'You are not in this chat'}))
                await self.close()
                return

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            messages = await self.get_messages(self.chat_id)

            for message in messages:
                await self.send(text_data=json.dumps({
                    'type': 'chat',
                    'message': message,
                }))
                if not message['is_read'] and message['author'] != self.user.id:
                    await self.read_message(message['id'])
        else:
            await self.close()

    async def receive(self, text_data):
        print(f'text_data:{text_data}')
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            user_id = text_data_json['user']
            file = text_data_json['file']
            user = await self.get_user(user_id)
            print(message, user)
            msg = await self.create_message(self.chat, user, message, file)
            print(msg)
            msg_data = ChatMessageSerializer(msg).data
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'new_message',
                    'message': msg_data,
                    'msg': msg,
                    'sender': user_id
                }
            )
        except Exception as e:
            self.disconnect()
        pass

    # паттерн наблюдатель один объект уведомляет другие

    async def new_message(self, event):
        message = event['message']
        print('shit')
        print(message)
        user = await self.get_user(event['message']['author'])
        if user != self.user:
            await self.read_message(message['id'])
        await self.send(text_data=json.dumps(
            {
                'type': 'new_message',
                'sender': user.username,
                'message': message,
            }
        )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


# -------------------------------------------------------------------
class ChatsConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_user_chats(self, user):
        return list(Chat.objects.filter(members__in=[user]))

    @database_sync_to_async
    def get_messages(self, chat_id=1):
        messages = ChatMessage.objects.filter(chat=chat_id)
        return [ChatMessageSerializer(messages).data for message in messages]

    @database_sync_to_async
    def get_user(self, user_id):
        return ChatUser.objects.get(id=user_id)

    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.chats = await self.get_user_chats(self.user)

            if not self.chats:
                await self.send(text_data=json.dumps({'error': 'You are not in any chat'}))
                await self.close()
                return

            self.chat = self.chats[0]

            self.room_group_name = f"{self.chat.id}"

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def receive(self):
        for chat in self.chats:
            new_messages = await self.get_messages(chat.id)
            last_message = await self.get_last_message(chat.id)
