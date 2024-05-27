from django.contrib import admin
from .models import *

admin.site.register(Chat)
admin.site.register(TextMessage)
admin.site.register(FileMessage)
admin.site.register(ImageMessage)
admin.site.register(VideoMessage)
admin.site.register(AudioMessage)
admin.site.register(StickerMessage)