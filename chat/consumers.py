import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .serializers import MessageSerializer
from .models import Message
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model


# sakht yek consumer va ers bari kardan az consumer websoketconsumer
class ChatConsumer(WebsocketConsumer):

    # vaghti k yek user payam khasi ra b samt server mifrestad in func
    # ejra mishavad va az message model sazi mikonad va data daryafti ra dar database zakhire mikonad
    def new_message(self, data):
        author_username = data['username']
        content = data["message"]
        author = get_user_model().objects.get(username=author_username)
        message_model = Message.objects.create(author=author, content=content)
        print("message model")
        message = self.message_serializer(message_model)
        message = eval(message)
        self.send_message_to_group(message)

    # ba harbar refresh shodan safhe message haye mojod refresh mishavand
    def fetch_message(self, data):
        roomname = data['roomname']
        qs = Message.get_last_messages(self, roomname)
        message_json = self.message_serializer(qs)
        content = {
            "message": eval(message_json),
            "command": "fetch_message"
        }
        self.chat_message(content)

    def message_serializer(self, qs):
        get_many = (lambda get_many: True if (qs.__class__.__name__ == 'QuerySet') else False)(qs)
        serializer = MessageSerializer(qs, many=get_many)
        message = JSONRenderer().render(serializer.data)
        return message

    # yek dict k command hayi k mishavad anjam dad ra darad va mitavanim ba estefade az an b function
    # hay neveshte shode dastresi dashte bashim
    commands = {
        "new_message": new_message,
        "fetch_message": fetch_message,
    }

    def connect(self):
        # scope etelaat darbareye connection darad
        # gereftan room_name az self.scope
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # gereftan group_name (group_name = chat_"room_name")
        self.room_group_name = "chat_%s" % self.room_name

        # join room group
        # ezafe kardan channel_name be group_name
        # channel_name auto tavasot chat consumer sakhte mishavad va faghat ma name an ra ba self.channelname migirim
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # ghabol cardan websoketconnection
        self.accept()

    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # daryaft data hayi k dar websoket baraye ma ersal mishavad
    def receive(self, text_data):
        # sakht yek dict json az datahaye daryafti
        text_data_json = json.loads(text_data)
        # joda kardan ghesmat message az text data
        message = text_data_json.get("message", None)
        command = text_data_json["command"]

        self.commands[command](self, text_data_json)

    def send_message_to_group(self, message):
        print(message)
        # ersal event b group
        async_to_sync(self.channel_layer.group_send)(
            # dar jeloye type esm function neveshte mishavad k event az an daryaft mishavad
            self.room_group_name,
            {
                "type": "chat_message",
                "content": message['content'],
                "command": 'new_message',
                "__str__": message['__str__']
             }
        )

    def chat_message(self, event):
        message = event["message"]
        # data json shode ra b websoket barmigardanad
        self.send(text_data=json.dumps({"message": message}))
















################################## BASE ##################################################################
# import json
#
# from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
#
#
# # sakht yek consumer va ers bari kardan az consumer websoketconsumer
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # scope etelaat darbareye connection darad
#         # gereftan room_name az self.scope
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         # gereftan group_name (group_name = chat_"room_name")
#         self.room_group_name = "chat_%s" % self.room_name
#
#         # join room group
#         # ezafe kardan channel_name be group_name
#         # channel_name auto tavasot chat consumer sakhte mishavad va faghat ma name an ra ba self.channelname migirim
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         # ghabol cardan websoketconnection
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # daryaft data hayi k dar websoket baraye ma ersal mishavad
#     #
#     async def receive(self, text_data):
#         # sakht yek dict json az datahaye daryafti
#         text_data_json = json.loads(text_data)
#         # joda kardan ghesmat message az text data
#         message = text_data_json["message"]
#
#         # ersal event b group
#         await self.channel_layer.group_send(
#             # dar jeloye type esm function neveshte mishavad k event az an daryaft mishavad
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )
#
#     async def chat_message(self, event):
#         message = event["message"]
#
#         # data json shode ra b websoket barmigardanad
#         await self.send(text_data=json.dumps({"message": message}))
