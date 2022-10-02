from multiprocessing import context
from django.shortcuts import render
from chat.models import Profile, Game
from django.contrib.auth.decorators import login_required
from django.db.models import Q




@login_required(login_url='login')
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    games = Game.objects.filter(
        Q(player_1=profile) |
        Q(player_2=profile)).order_by('-id')

    waiting = Game.objects.filter(status='W').order_by('-id')
    active = Game.objects.filter(status='A').order_by('-id')
    processing = Game.objects.filter(status='P').order_by('-id')
    finished = Game.objects.filter(status='F').order_by('-id')


    context = {'games': games, 'processing_games': processing, 'finished_games': finished, 'waiting_games': waiting, 'active_games': active, 'username': profile.user.username, 'user_id': profile.user.id}
    return render(request, 'dashboard/dashboard.html', context=context)