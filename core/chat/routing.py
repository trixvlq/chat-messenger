from django.urls import path
from .consumers import *

ws_urlpatterns = [
    path('ws/chats/', ChatConsumer.as_asgi()),
    path('ws/chat/<int:chat_id>/', ChatConsumer.as_asgi()),
]
