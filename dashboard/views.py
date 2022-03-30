from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from game.models import *


@login_required(login_url='login')
def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)
    games = Game.objects.filter(
        Q(player_1=profile) |
        Q(player_2=profile)).order_by('-id')

    waiting = Game.objects.filter(status='W').order_by('-id')
    active = Game.objects.filter(status='A').order_by('-id')

    context = {'games': games, 'waiting_games': waiting, 'active_games': active, 'user': profile.user.username, 'user_id': profile.user.id}
    return render(request, 'dashboard/index.html', context=context)
