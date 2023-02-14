import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.shortcuts import get_object_or_404


class ChatConsumers(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["pk"]
        print(self.room_group_name)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        print(self.channel_name)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_id = text_data_json["user"]
        user = get_object_or_404(Account, id=user_id)
        chat = get_object_or_404(Chat, id=int(self.room_group_name))
        # print(message)
        print(message)
        Message(user=user, chat=chat, content=message).save()
        # user = User.objects.get(id=user)
        # chat_id = Chat.objects.get(id=text_data_json["chat_id"])
        # form = Message(user=user, content=message, chat=chat_id)
        # form.save()
        # print(text_data_json['user'])
        #
        print(self.channel_name)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': user.id,
                'message': message
            }
        )

    def chat_message(self, event):
        print(self.room_group_name)
        message = event['message']
        user_id = event["user"]
        print(user_id)
        user = get_object_or_404(Account, id=user_id)

        self.send(text_data=json.dumps(
            {
                'type': 'chat',
                'message': message,
                'user': user.username
            }
        ))
