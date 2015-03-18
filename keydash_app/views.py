from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.models import User
from keydash_app.models import Score, UserProfile, Game
from keydash_app.forms import UserForm, UserProfileForm

from django.http import HttpResponse, HttpResponseRedirect

def about(request):
    return render(request, 'keydash_app/about.html')

def index(request):
    if request.user.is_authenticated():
        context_dict = {}
        user_list_by_last_login = User.objects.order_by('-last_login')
        context_dict['users'] = user_list_by_last_login
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

    user_scores = Score.objects.filter(user = user).order_by('-score')
    context_dict['scores'] = user_scores

    if request.method == 'POST':
        game_mode = request.POST.get('dropdown_game_mode')
        game_mode = Game.objects.get(game_mode = game_mode)
        user_scores_for_game_mode = Score.objects.filter(user = user, game = game_mode).order_by('-score')
        context_dict['game_mode'] = game_mode
        context_dict['user_scores_for_game_mode'] = user_scores_for_game_mode

    return render(request, 'keydash_app/statistics_personal.html', context_dict)

def statistics_global(request):
    context_dict = {}
    user_list_by_ranking = UserProfile.objects.order_by('ranking_position')
    context_dict['users'] = user_list_by_ranking

    if request.method == 'POST':
        game_mode = request.POST.get('dropdown_game_mode')
        game_mode = Game.objects.get(game_mode = game_mode)
        user_scores_for_game_mode = Score.objects.filter( game = game_mode).order_by('-score')
        context_dict['game_mode'] = game_mode
        context_dict['user_scores_for_game_mode'] = user_scores_for_game_mode

    return render(request, 'keydash_app/statistics_global.html', context_dict)

def profile(request):
    context_dict = {}
    user = request.user
    user_profile = UserProfile.objects.get(user = user)

    if request.method == 'POST':
        profile_form = UserProfileForm(data = request.POST, instance = user_profile)
        user_form = UserForm(request.POST, instance = user)

        if profile_form.is_valid() and user_form.is_valid():
            user_profile = profile_form.save(commit=False)
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            # if user_form.has_changed():
            #     user_form.save()
            user_profile.save()
            user_form.save()
            user.save()
            return HttpResponseRedirect('/keydash/profile/')
    else:
        context_dict['user_profile'] = user_profile
        profile_form = UserProfileForm()
        context_dict['profile_form'] = profile_form
        user_form = UserForm()
        context_dict['user_form'] = user_form

    return render(request, 'keydash_app/profile.html', context_dict)


def register_profile(request):

    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user_id = request.user.id
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            return HttpResponseRedirect('/keydash/')
        else:
            print profile_form.errors
    else:
        profile_form = UserProfileForm()

    return render(request, 'keydash_app/profile_registration.html', {'profile_form': profile_form })
