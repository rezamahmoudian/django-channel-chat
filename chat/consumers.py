import json

from channels.generic.websocket import WebsocketConsumer


# sakht yek consumer va ers bari kardan az consumer websoketconsumer
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    # daryaft data hayi k dar websoket baraye ma ersal mishavad
    #
    def receive(self, text_data):
        # sakht yek dict json az datahaye daryafti
        text_data_json = json.loads(text_data)
        # joda kardan ghesmat message az text data
        message = text_data_json["message"]

        # data json shode ra b websoket barmigardanad
        self.send(text_data=json.dumps({"message": message}))
