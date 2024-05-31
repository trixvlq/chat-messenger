from django import template

from chat.query_helpers import get_all_messages

register = template.Library()

@register.filter
def get_unread_messages(chat, user):
    unread = 0
    messages = get_all_messages(chat.id)
    for message in messages:
        if not message.is_read and message.author != user:
            unread += 1
    return unread