import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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


    def get_players(self):
        game = Game.objects.filter(id=self.room_name)
        if game:
            print("the game was found")
            game = game[0]
            if game.player_2 is not None:
                return (
                    game.player_1.user.username,
                    game.player_2.user.username,
                )
            if game.player_1 is not None:
                return (
                    game.player_1.user.username,
                )
        print("the game wasn't found")
        return None


    def get_word(self, word):
        print(word)
        print(self.room_name)
        game = Game.objects.get(id=self.room_name)
        category = game.task.category
        player = Profile.objects.get(user=self.sender)
        word_db = Word.objects.filter(word=word, category=category)

        print(word_db, category, game, player)

        if word == 'lyalyalya':
            return {'status': 'startgame'}

        else:
            return {
                'status': 'success',
                'message': 'The word "{}" was successfully added to the game'.format(word)
            }
            


    # Receive message from WebSocket
    def receive(self, text_data):
        print('potatoes')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # print(self.scope)
        # print(self.scope["user"])
        self.sender = self.scope["user"]


        self.word_db = self.get_word(message)
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