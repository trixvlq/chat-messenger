from django.contrib import admin
from .models import *


class ChatUserAdmin(admin.ModelAdmin):
    model = ChatUser
    fields = ('username', 'first_name', 'last_name', 'email', 'password')
    list_display = ('username', 'first_name', 'last_name', 'email', 'password')
    list_filter = ('username', 'first_name', 'last_name', 'email', 'password')

admin.site.register(ChatUser)
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(SearchSession)
admin.site.register(FriendRequest)
