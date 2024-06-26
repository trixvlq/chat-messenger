from rest_framework import serializers
from .models import *


# паттерн DTO
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = ChatMessage
        fields = ['id', 'chat', 'author', 'author_name', 'content', 'date_sent', 'is_read', 'file']

    def get_author_name(self, obj):
        return obj.author.nickname


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = '__all__'
