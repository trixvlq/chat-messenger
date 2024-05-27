from rest_framework import serializers
from .models import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class TextMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = TextMessage
        fields = ['id', 'chat', 'author', 'content', 'date_sent', 'is_read', 'sender']

    def get_sender(self,obj):
        return obj.author.username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
