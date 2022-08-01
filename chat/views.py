from django.http import HttpResponse
from django.shortcuts import render
import random
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response

import datetime
from django.utils.timezone import now


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


def game_view(request, game_id):
    print('проверка вьюшки')
    """
    Если метод запроса это post(если функция принимает отправленное слово),
    то достаются параметры данного слова(пользователь и само слово) из api используя вьюшку GameWordView
    """

    if request.method == 'GET':
        #А так же достается id игры для того чтобы подставить его в ссылку страницы которую мы после отображаем
        return render(request, 'chat/room.html', context={'data': {'id':game_id}})

    

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




class GameView(APIView):
    #Создаем функцию get которая принимает на вход id игры и контекст в виде request и с помощью этого достает слова для каждого игрока
    def get(self, request, game_id):
        print('проверка апи')
        try:
            # game_id = request.query_params.get('game_id')
            # создаем список с одним элементом игры, так как только у одной может быть подходящий id
            game = Game.objects.filter(id=game_id)
            #Если в этом списке есть игра(если такая игра нашлась)
            if game:
                print(game[0].player_1, game[0].player_2)
                


                #Создаем переменную serializer которая достает данные о нужной нам игре в правильном формате
                serializer = GameSerializer(game[0], context={'request': request})
                # print(serializer.data)
                #Сначала создаем список со словами которые находятся в правильной игре и у нужно нам игрока
                words_1 = GameWord.objects.filter(game=game[0], player=game[0].player_1)
                #Мы создаем пустой список который будет содержать только текстовый вид самого слова без дополнительной информации
                words_1_list = []
                for w in words_1:
                    words_1_list.append(w.word.word)

                #Повторяем процесс для списка слов второго игрока
                words_2 = GameWord.objects.filter(game=game[0], player=game[0].player_2)
                words_2_list = []
                for w in words_2:
                    words_2_list.append(w.word.word)

                #Создаем переменную response которая будет содержать все данные из ранее полученных данных об игре(задание и оба игрока)
                response = serializer.data
                #После этого добавляем полученные списки слов к данным об игре
                response['words_1'] = words_1_list
                response['words_2'] = words_2_list
                #Возвращаем response который позже будет отрисован функцией game_view
                return Response(response)

            #Если такая игра не найдена, выводим ошибку об этой ситуации
            return Response({'status': 'error',
                             'error': 'game with id {} not found'.format(game_id)})
        #В случае ошибки возвращаем текст который сообщает о проблеме
        except Exception as e:
            return Response({'status': 'error',
                             'error': str(e)})


    def put(self, request, game_id):
        print('helloworldagain')
        game = Game.objects.filter(id=game_id)
        if game and game[0].player_1 is not None and game[0].player_2 is None:
            game = game[0]
            game.status = 'A'
            
            user_id = request.data['user_id']
            user = Profile.objects.get(user=user_id)
            game.player_2 = user

            game.end_time = now()+datetime.timedelta(0, game.task.time)
            game.save()

            serializer = GameSerializer(game)
            data = serializer.data
            print(data)
            return Response(data, status=200)
        
        else:
            return Response({'status': 'error',
                             'error': 'There was an error oops'})
