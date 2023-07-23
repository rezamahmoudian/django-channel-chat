import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


# sakht yek consumer va ers bari kardan az consumer websoketconsumer
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # scope etelaat darbareye connection darad
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = "chat_%s" % self.room_name

        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # daryaft data hayi k dar websoket baraye ma ersal mishavad
    #
    def receive(self, text_data):
        # sakht yek dict json az datahaye daryafti
        text_data_json = json.loads(text_data)
        # joda kardan ghesmat message az text data
        message = text_data_json["message"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

        def chat_message(self, event):
            message = event["message"]

            # data json shode ra b websoket barmigardanad
            self.send(text_data=json.dumps({"message": message}))


