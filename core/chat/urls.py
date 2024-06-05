from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('<int:chat_id>/', chat, name='chat'),
    path('dima/',dima),
    path('test/',test),
]
