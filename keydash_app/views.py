from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.models import User
from keydash_app.models import UserProfile

from django.http import HttpResponse

def about(request):
    return render(request, 'keydash_app/about.html')

def index(request):

    context_dict = {'boldmessage': "I am bold font from the context"}
    if request.user.is_authenticated():
        r = render(request, 'keydash_app/home.html', context_dict)
    else:
        r = render(request, 'keydash_app/front.html')
    return r

def front(request):
    return render(request, 'keydash_app/front.html')

def trial(request):
    return render(request, 'keydash_app/trial_game.html')

def game(request):
    return render(request, 'keydash_app/game.html')

def statistics(request):
    return render(request, 'keydash_app/statistics.html')

def statistics_personal(request):
    context_dict = {}
    user = request.user
    user_profile = UserProfile.objects.get(user = user)
    context_dict['user_profile'] = user_profile
    return render(request, 'keydash_app/statistics_personal.html', context_dict)

def statistics_global(request):
    context_dict = {}
    user_list_by_ranking = UserProfile.objects.order_by('ranking_position')
    context_dict['users'] = user_list_by_ranking
    return render(request, 'keydash_app/statistics_global.html', context_dict)

def profile(request):
    context_dict = {}
    user = request.user
    user_profile = UserProfile.objects.get(user = user)
    context_dict['user_profile'] = user_profile
    return render(request, 'keydash_app/profile.html', context_dict)
