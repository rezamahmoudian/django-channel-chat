# Generated by Django 4.2.3 on 2023-07-28 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_related_chat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='roomname',
            new_name='room_name',
        ),
    ]
