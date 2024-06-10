from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('<int:chat_id>/', chat, name='chat'),
    path('test/',test, name='main'),
    path('login/',register_view, name='register'),
    path('register/',login_view, name='login'),
    path('upload-file/<int:chat_id>/', upload_file, name='upload-file'),
]
