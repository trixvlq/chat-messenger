from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('<int:chat_id>/', chat, name='chat'),
<<<<<<< HEAD
=======
    path('dima/',dima),
>>>>>>> 91b8fb9c46e6de286d649d7eed847616e0c33392
    path('test/',test),
]
