from django.urls import path
from .views import *

urlpatterns = [
    path('', test, name='main'),
    path('<int:chat_id>/', chat, name='chat'),
    path('login/',login_view, name='login'),
    path('register/',register_view, name='register'),
    path('upload-file/<int:chat_id>/', upload_file, name='upload-file'),
    path('change_credentials/', change_credentials, name='change_credentials'),
    path('logout/', logout_view, name='logout'),
    path('search/', search, name='search'),
    path('user_info/<int:user_id>/', user_info, name='user_info'),
]
