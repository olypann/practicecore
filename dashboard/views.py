from multiprocessing import context
from django.shortcuts import render
from chat.models import Profile

# Create your views here.
def dashboard(request):
    # context = {'user': profile.user.username}
    context = {}
    return render(request, 'dashboard/dashboard.html', context)
