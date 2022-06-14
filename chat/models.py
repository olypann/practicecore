from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_player = models.BooleanField(default=True)
    is_creator = models.BooleanField(default=False)
    is_validator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    time = models.IntegerField(default=120)
    letter = models.CharField(max_length=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.category) + ' ' + str(self.letter).upper()


class Word(models.Model):
    word = models.CharField(max_length=50)
    points = models.IntegerField(default=-1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.word) + " (" + str(self.category) + "), " + str(self.points)


class Status(models.TextChoices):
    WAITING = 'W', 'Waiting'
    ACTIVE = 'A', 'Active'
    PROCESSING = 'P', 'Processing'
    FINISHED = 'F', 'Finished'


class Game(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(Profile, related_name='player_1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey(Profile, related_name='player_2', on_delete=models.CASCADE, null=True, blank=True)
    words = models.ManyToManyField(Word, through='GameWord')
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.WAITING)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.task) + ', ' + str(self.player_1) + ' vs ' + str(self.player_2) + ', ' + str(self.status)


class GameWord(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.game) + ', ' + str(self.word) + ', ' + str(self.player)


