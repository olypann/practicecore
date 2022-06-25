from multiprocessing import context
from django.shortcuts import render
from chat.models import Profile, Game
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
# def dashboard(request):
#     # context = {'user': profile.user.username}
#     context = {}
#     return render(request, 'dashboard/dashboard.html', context)

# @login_required(login_url='login')
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    games = Game.objects.filter(
        Q(player_1=profile) |
        Q(player_2=profile)).order_by('-id')

    waiting = Game.objects.filter(status='W').order_by('-id')
    active = Game.objects.filter(status='A').order_by('-id')

    context = {'games': games, 'waiting_games': waiting, 'active_games': active, 'user': profile.user.username, 'user_id': profile.user.id}
    return render(request, 'dashboard/dashboard.html', context=context)