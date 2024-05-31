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

class ImageMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = ImageMessage
        fields = ['id', 'chat', 'author', 'image', 'date_sent', 'is_read', 'sender']

    def get_sender(self,obj):
        return obj.author.username

class FileMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = FileMessage
        fields = ['id', 'chat', 'author', 'file', 'date_sent', 'is_read', 'sender']

    def get_sender(self,obj):
        return obj.author.username

class VideoMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = VideoMessage
        fields = ['id', 'chat', 'author', 'video', 'date_sent', 'is_read', 'sender']

    def get_sender(self,obj):
        return obj.author.username

class AudioMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = AudioMessage
        fields = ['id', 'chat', 'author', 'audio', 'date_sent', 'is_read', 'sender']

    def get_sender(self,obj):
        return obj.author.username

class StickerMessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    class Meta:
        model = StickerMessage
        fields = ['id', 'chat', 'author', 'sticker', 'date_sent', 'is_read', 'sender']

    def get_sender(self,obj):
        return obj.author.username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
