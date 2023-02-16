import datetime
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
        print('da')
        mess = Message(user=user, chat=chat, content=message).save()
        now = datetime.datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print(current_time)

        # user = User.objects.get(id=user)
        # chat_id = Chat.objects.get(id=text_data_json["chat_id"])
        # form = Message(user=user, content=message, chat=chat_id)
        # form.save()
        # print(text_data_json['user'])
        #
        print(self.channel_name)
        print(user.first_name)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': user.id,
                'message': message,
                'time': str(current_time),
                'full_name': user.first_name + ' ' + user.last_name,
            }
        )

    def chat_message(self, event):
        print(self.room_group_name)
        message = event['message']
        user_id = event["user"]
        print(user_id)
        user = get_object_or_404(Account, id=user_id)
        mess = message
        now = datetime.datetime.now()
        if user.image:
            user_image = str(user.image.url)
        else:
            user_image = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460__340.png'
        current_time = now.strftime("%H:%M:%S")

        self.send(text_data=json.dumps(
            {
                'type': 'chat',
                'message': message,
                'user': user.username,
                'time': str(current_time),
                'image': str(user_image),
                'user_id': str(user.id),
                'full_name': user.first_name + ' ' + user.last_name,
            }
        ))
