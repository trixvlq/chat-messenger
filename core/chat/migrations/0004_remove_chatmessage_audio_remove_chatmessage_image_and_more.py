# Generated by Django 5.0.6 on 2024-06-10 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_chatmessage_audio_alter_chatmessage_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='audio',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='video',
        ),
    ]