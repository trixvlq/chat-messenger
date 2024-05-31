from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import *
from .serializers import *


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_chat(self, chat_id=1):
        return Chat.objects.get(id=chat_id)

    @database_sync_to_async
    def get_messages(self, chat_id):
        messages = TextMessage.objects.filter(chat=chat_id)
        return TextMessageSerializer(messages, many=True).data

    @database_sync_to_async
    def create_message(self, chat, user, message):
        return TextMessage.objects.create(
            chat=chat,
            author=user,
            content=message
        )

    @database_sync_to_async
    def if_user_in_chat(self, user, chat):
        return user in chat.members.all()

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def read_message(self, message):
        if message.is_read == False and message.author != self.user:
            message.is_read = True
            message.save()

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope["user"]
        self.messages = await self.get_messages(self.chat_id)

        if self.user.is_authenticated:
            self.chat = await self.get_chat(self.chat_id)
            self.room_group_name = f'{self.chat_id}'

            if not self.chat:
                await self.send(text_data=json.dumps({'error': 'Chat does not exist'}))
                await self.close()
                return

            if not self.if_user_in_chat(self.user, self.chat):
                await self.send(text_data=json.dumps({'error': 'You are not in this chat'}))
                await self.close()
                return

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            for message in self.messages:
                await self.send(text_data=json.dumps(
                    {
                        'type': 'chat',
                        'sender': message['sender'],
                        'message': message['content'],
                    }
                ))

    async def receive(self, text_data):
        try:
            print(f'shit')
            print(text_data)
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            user_id = text_data_json['user']
            user = await self.get_user(user_id)
            msg = await self.create_message(self.chat, user, message)
            msg = TextMessageSerializer(msg).data
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'new_message',
                    'message': msg,
                    'sender': user_id
                }
            )
        except Exception as e:
            self.disconnect()
        pass

    async def new_message(self, event):
        print('chat')
        message = event['message']
        user_id = event['sender']
        user = await self.get_user(user_id)
        # if user != self.user:
        #     await self.read_message(TextMessage.objects.get(id=message))
        await self.send(text_data=json.dumps(
            {
                'type': 'new_message',
                'sender': user.username,
                'message': message,
            }
        )
        )


# -------------------------------------------------------------------
class ChatsConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_user_chats(self, user):
        return list(Chat.objects.filter(members__in=[user]))

    @database_sync_to_async
    def get_messages(self, chat_id=1):
        messages = TextMessage.objects.filter(chat=chat_id)
        return [TextMessageSerializer(messages).data for message in messages]

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

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

            self.messages = self.get_messages(self.chat.id)

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)

            message = text_data_json['message']

            user_id = text_data_json['user']

            sending_user = await self.get_user(user_id)

            message = await self.create_message(self.chat, sending_user, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'sender': user_id,
                    'message': message.content
                }
            )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON'}))
            await self.close()
            return

        except Exception as e:
            await self.send(text_data=json.dumps({'error': f'{str(e)} shit'}))
            await self.close()
            return

    async def chat_message(self, event):
        message = event['message']
        user_id = event['sender']
        user = await self.get_user(user_id)
        await self.send(text_data=json.dumps(
            {
                'type': 'chat',
                'sender': user.username,
                'message': message,
            }
        )
        )
