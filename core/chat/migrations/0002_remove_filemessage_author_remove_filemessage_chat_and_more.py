# Generated by Django 5.0.6 on 2024-06-01 09:09

import chat.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filemessage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='filemessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='imagemessage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='imagemessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='stickermessage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='stickermessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='textmessage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='textmessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='videomessage',
            name='author',
        ),
        migrations.RemoveField(
            model_name='videomessage',
            name='chat',
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('content', models.TextField()),
                ('file', models.FileField(upload_to=chat.models.upload_file)),
                ('image', models.ImageField(upload_to=chat.models.upload_file)),
                ('video', models.FileField(upload_to=chat.models.upload_file)),
                ('audio', models.FileField(upload_to=chat.models.upload_file)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
            ],
        ),
        migrations.DeleteModel(
            name='AudioMessage',
        ),
        migrations.DeleteModel(
            name='FileMessage',
        ),
        migrations.DeleteModel(
            name='ImageMessage',
        ),
        migrations.DeleteModel(
            name='StickerMessage',
        ),
        migrations.DeleteModel(
            name='TextMessage',
        ),
        migrations.DeleteModel(
            name='VideoMessage',
        ),
    ]