from itertools import chain
from operator import attrgetter

from .models import *

def get_all_messages(chat_id):
    chat = Chat.objects.get(id=chat_id)
    texts = TextMessage.objects.filter(chat=chat_id)
    images = ImageMessage.objects.filter(chat=chat_id)
    files = FileMessage.objects.filter(chat=chat_id)
    videos = VideoMessage.objects.filter(chat=chat_id)
    audios = AudioMessage.objects.filter(chat=chat_id)
    stickers = StickerMessage.objects.filter(chat=chat_id)

    all_messages = sorted(
        chain(texts, images, files, videos, audios, stickers),
        key=attrgetter('date_sent')
    )

    return all_messages