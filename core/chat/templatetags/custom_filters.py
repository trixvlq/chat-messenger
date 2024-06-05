from django import template

from chat.models import *

register = template.Library()

@register.filter
def get_unread_messages(chat, user):
    unread = 0
    messages = ChatMessage.objects.filter(chat=chat.id)
    for message in messages:
        if not message.is_read and message.author != user:
            unread += 1
    return unread