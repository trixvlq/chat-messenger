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


@register.filter
def get_other_pfp(chat,current_user):
    for user in chat.members.all():
        if user != current_user:
            return user.pfp.url

@register.filter
def get_last_message(chat):
    msg = ChatMessage.objects.filter(chat=chat).last()
    if msg != None:
        return msg
    else:
        return f'Начните беседу с {chat}'

@register.filter
def get_last_date(chat):
    last_msg = get_last_message(chat)
    if last_msg != f'Начните беседу с {chat}':
        return last_msg.date_sent
    else:
        return ''