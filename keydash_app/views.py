from django.shortcuts import render
from django.shortcuts import redirect


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

def profile(request):
    return render(request, 'keydash_app/profile.html')