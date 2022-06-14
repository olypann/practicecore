from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    creator = ProfileSerializer()

    class Meta:
        model = Category
        fields = '__all__'


class WordSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    approved_by = ProfileSerializer()

    class Meta:
        model = Word
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Task
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    player_1 = ProfileSerializer()
    player_2 = ProfileSerializer()

    class Meta:
        model = Game
        fields = ['id', 'task', 'player_1', 'player_2', 'status', 'end_time']


class GameWordSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    word = WordSerializer()
    player = ProfileSerializer()

    class Meta:
        model = GameWord
        fields = '__all__'
