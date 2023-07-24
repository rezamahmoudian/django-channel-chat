import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


# sakht yek consumer va ers bari kardan az consumer websoketconsumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # scope etelaat darbareye connection darad
        # gereftan room_name az self.scope
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # gereftan group_name (group_name = chat_"room_name")
        self.room_group_name = "chat_%s" % self.room_name

        # join room group
        # ezafe kardan channel_name be group_name
        # channel_name auto tavasot chat consumer sakhte mishavad va faghat ma name an ra ba self.channelname migirim
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # ghabol cardan websoketconnection
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # daryaft data hayi k dar websoket baraye ma ersal mishavad
    #
    async def receive(self, text_data):
        # sakht yek dict json az datahaye daryafti
        text_data_json = json.loads(text_data)
        # joda kardan ghesmat message az text data
        message = text_data_json["message"]

        # ersal event b group
        await self.channel_layer.group_send(
            # dar jeloye type esm function neveshte mishavad k event az an daryaft mishavad
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        # data json shode ra b websoket barmigardanad
        await self.send(text_data=json.dumps({"message": message}))
