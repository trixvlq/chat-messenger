from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import *
from .serializers import *


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def create_message(self, chat, user, message):
        return TextMessage.objects.create(
            chat=chat,
            author=user,
            content=message
        )

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
        print(self.scope)
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
