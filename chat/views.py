from django.http import HttpResponse
from django.shortcuts import render
import random
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response



def room(request, room_name):
    try:
        print(room_name)
        game = Game.objects.get(id=int(room_name))

        game_data = GameSerializer(game).data

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'game': game_data,
        })

    except:
        return HttpResponse(f'game {room_name} not found!')

class NewGameView(APIView):
    def post(self, request):
        print('waiting class 2')
        try:
            letter = random.choice(['P', 'B', 'K', 'S'])
            category = random.choice(Category.objects.all())
            task = Task.objects.create(letter=letter, category=category)

            print(request.data)
            
            user_id = request.data['user_id']
            print(user_id)
            user = Profile.objects.get(user=user_id)

            game = Game.objects.create(task=task, player_1=user)
            game_data = GameSerializer(game).data
            return Response(game_data, status=201)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=500)