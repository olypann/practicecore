import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.user = self.scope["user"]
        self.user_room_name = f"notif_room_for_user_{self.user.id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        players = self.get_players()
        print(players)


        if len(players) == 2:
           async_to_sync(self.channel_layer.group_send)(
                self.user_room_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'current_player': self.user.username,
                        'enemy': [p for p in players if p != self.user.username][0],
                        'type': 'players',
                    },
                }
            )


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # print(self.scope)
        # print(self.scope["user"])
        self.sender = self.scope["user"]


        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         # 'message': message
        #         'message': {'text': f"{message}", 'type': 'success', 'sender': f"{self.sender}"},
        #     }
        # )
        
        self.word_db = async_to_sync(self.get_word)(message)
        if self.word_db:
            if self.word_db["status"] == "error":
                async_to_sync(self.channel_layer.group_send)(
                    self.user_room_name,
                    {
                        'type': 'chat_message',
                        'message': {'text': self.word_db["error"], 'type': 'error'},
                    }
                )

            elif self.word_db["status"] == "startgame":
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': {'type': 'startgame', 'sender': f"{self.sender}"}
                    }
                )

            elif self.word_db["status"] == "success":
                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': {'text': f"{message}", 'type': 'success', 'sender': f"{self.sender}"}
                    }
                )







    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))