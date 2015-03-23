import random
import string
import urllib, urllib2, json
import datetime

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.models import User
from keydash_app.models import Score, UserProfile, Game
from friendship.models import Friend, FriendshipRequest
from keydash_app.forms import UserForm, UserProfileForm
from chartit import DataPool, Chart

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def about(request):
    return render(request, 'keydash_app/about.html')

def index(request):
    if request.user.is_authenticated():
        context_dict = {}
        user_list_by_last_login = User.objects.order_by('-last_login')
        context_dict['users'] = user_list_by_last_login
        context_dict.update( statistics_chart(request) )
        r = render(request, 'keydash_app/home.html', context_dict)
    else:
        r = render(request, 'keydash_app/front.html')
    return r

def front(request):
    return render(request, 'keydash_app/front.html')

def trial(request):
    context_dict = {'game_js': ["trial.js"], 'game_css':"textgame.css"}
    return render(request, 'keydash_app/trial_game.html', context_dict)


@login_required
def game(request):
    game_mode = request.GET.get('game_mode', '')
    game = get_object_or_404(Game, game_mode = game_mode)
    context_dict = {'game_js': game.game_js.split(','), 'game_css':game.game_css}
    return render(request, 'keydash_app/game.html', context_dict)

def is_word_english(word):
    try:
        word.encode('ascii')
    except UnicodeEnecodeError:
        return False
    else:
        return True    

def game_get_new_data(request, game_mode):
    if(game_mode == 'paragraph'):
        resp_data = {'words': [(''.join(random.choice(string.ascii_letters + string.punctuation + "0123456789" + " ") for i in range(160))) for x in range(20)] }
    elif(game_mode == 'rand_alpha'):
        resp_data = {'words': [(''.join(random.choice(string.ascii_letters + "0123456789") for i in range(16))) for x in range(20)] }
    elif(game_mode == 'rand_alpha_punc'):
        resp_data = {'words': [(''.join(random.choice(string.ascii_letters + string.punctuation + "0123456789") for i in range(16))) for x in range(20)] }
    else:
        resp_data = {'words': [x['word'] for x in game_request_new_data()]}
    return JsonResponse(resp_data)

def game_request_new_data():
    url = "http://api.wordnik.com:80/v4/words.json/randomWords?hasDictionaryDef=true&minCorpusCount=0&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=5&maxLength=-1&limit=20&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5"
    return json.load(urllib2.urlopen(url))

def game_add_new_score(request, game_mode, wpm, accuracy, score = None):
    game = Game.objects.get(game_mode = game_mode)
    
    if score == None :
        score = float(wpm) * float(accuracy)

    Score.objects.create(user = request.user,
                                        game = game,
                                        wpm = float(wpm),
                                        accuracy = float(accuracy),
                                        score = score,
                                        date = datetime.datetime.now())

    user_profile = UserProfile.objects.get(user = request.user)
    wpm_highest = user_profile.wpm_highest
    accuracy_highest = user_profile.accuracy_highest
    score_highest = user_profile.score_highest
    if (float(wpm) > wpm_highest):
        user_profile.wpm_highest = float(wpm)

    if (score > score_highest):
        user_profile.score_highest = score

    if (float(accuracy) > accuracy_highest):
        user_profile.accuracy_highest = float(accuracy)

    user_profile.save()

    return JsonResponse({'success': "true"})


@login_required
def statistics_personal(request):
    context_dict = {}
    user = request.user
    user_profile = UserProfile.objects.get(user = user)
    context_dict['user_profile'] = user_profile

    # filters all the scores of the user in descending order
    user_scores = Score.objects.filter(user = user).order_by('-score')
    for user_score in user_scores:
        # for every score it takes its game mode, transforms it into readable name and then saves asn readable game mode
        readable_game_mode = (game_mode_readable_name(user_score.game))
        # changes the name of the each game mode for every score
        user_score.game.game_mode = readable_game_mode['game_mode']
    context_dict['scores'] = user_scores

    if request.method == 'POST':
        game_mode = request.POST.get('dropdown_game_mode')
        game = Game.objects.get(game_mode = game_mode)
        context_dict.update( statistics_chart2(request, game) )
        user_scores_for_game_mode = Score.objects.filter(user = user, game = game).order_by('-score')

        # saving readable game mode names, later on used to display in template
        context_dict.update( game_mode_readable_name(game))
        context_dict['user_scores_for_game_mode'] = user_scores_for_game_mode

    else:
        context_dict.update( statistics_chart(request) )

    return render(request, 'keydash_app/statistics_personal.html', context_dict)


@login_required
def statistics_global(request):
    context_dict = {}
    user_list_by_ranking = UserProfile.objects.order_by('ranking_position')
    context_dict['users'] = user_list_by_ranking

    if request.method == 'POST':
        game_mode = request.POST.get('dropdown_game_mode')
        game_mode = Game.objects.get(game_mode = game_mode)
        user_scores_for_game_mode = Score.objects.filter( game = game_mode).order_by('-score')

        # saving readable game mode names, later on used to display in template
        context_dict.update( game_mode_readable_name(game_mode))
        context_dict['user_scores_for_game_mode'] = user_scores_for_game_mode

    return render(request, 'keydash_app/statistics_global.html', context_dict)


@login_required
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

            data = user_form.cleaned_data
            email = data['email']
            if email != '':
                user_form.save()
                user.save()
            user_profile.save()

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
            return HttpResponseRedirect('/keydash/friends_keydash/')
        else:
            print profile_form.errors
    else:
        profile_form = UserProfileForm()

    return render(request, 'keydash_app/profile_registration.html', {'profile_form': profile_form })


@login_required
def friends_keydash(request, username=None):
    context_dict = {}
    user = request.user
    friends = Friend.objects.friends(user)

    profiles = []
    for friend in friends:
        try:
            profile = UserProfile.objects.get(user = friend)
            profiles.append(profile)
        except UserProfile.DoesNotExist:
            pass

    context_dict['profiles'] = profiles


    #dispalying all the other users
    other_users = []
    all_users = User.objects.exclude(username = user.username)
    for user in all_users:
        if user not in friends:
            other_users.append(user)

    context_dict['other_users'] = other_users

    return render(request, 'keydash_app/friends_keydash.html', context_dict)



@login_required
def friends_requests_keydash(request):
    context_dict = {}
    user = request.user
    # List all unread friendship requests
    requests = FriendshipRequest.objects.filter(rejected__isnull=True, to_user=user)
    print requests
    context_dict['requests'] = requests
    return render(request, 'keydash_app/friends_requests_keydash.html', context_dict)


@login_required
def friendship_accept_keydash(request, friendship_request_id):
    if request.method == 'POST':
        f_request = get_object_or_404(request.user.friendship_requests_received,id=friendship_request_id)
        f_request.accept()
        return HttpResponseRedirect('/keydash/friends_keydash')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


@login_required
def friendship_reject_keydash(request, friendship_request_id):
    if request.method == 'POST':
        f_request = get_object_or_404(request.user.friendship_requests_received,id=friendship_request_id)
        f_request.delete()
        return HttpResponseRedirect('/keydash/friends_keydash')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


def game_mode_readable_name(game):
    context_dict = {}
    if(game.game_mode == 'eng_dict'):
        context_dict['game_mode'] = 'English Dictionary'
    elif(game.game_mode == 'rand_alpha'):
        context_dict['game_mode'] = 'Random Alphanumeric'
    elif(game.game_mode == 'typingflight'):
        context_dict['game_mode'] = 'Typing Fight'
    elif(game.game_mode == 'rand_alpha_punc'):
        context_dict['game_mode'] = 'Random Alphanumeric + Punctuation'
    else:
        context_dict['game_mode'] = 'Paragraph'
    return context_dict

def statistics_chart(request):
    context_dict = {}
    user = request.user
    # Create a DataPool with the data we want to retrieve.
    game_data = \
        DataPool(
           series=
            [{'options': {
               'source': Score.objects.filter(user = user)},
              'terms': [
                'id',
                'date',
                'score']}
             ])

    def change_from_score_id_to_date(month_num):
        score_object = Score.objects.get(id=month_num)
        date_from_score = score_object.date.strftime('%d-%b-%Y %H:%M:%S')
        return str(date_from_score)

    # Create the Chart object
    cht = Chart(
        datasource = game_data,
        series_options =
          [{'options':{
              'type': 'column',
              'stacking': True},
            'terms':{
              'id': [
                'score']
              }}],
        chart_options =
          {'title': {
               'text': 'Statistics'},
           'xAxis': {
                'title': {
                   'text': 'Games'}}},
        x_sortf_mapf_mts = (None, change_from_score_id_to_date, False))

    context_dict['chart'] = cht
    return context_dict

def statistics_chart2(request, game):
    context_dict = {}
    user = request.user
    # Create a DataPool with the data we want to retrieve.
    game_data = \
        DataPool(
           series=
            [{'options': {
               'source': Score.objects.filter(user = user, game = game)},
              'terms': [
                'id',
                'date',
                'score']}
             ])

    def change_from_score_id_to_date(month_num):
        score_object = Score.objects.get(id=month_num)
        date_from_score = score_object.date.strftime('%d-%b-%Y %H:%M:%S')
        return str(date_from_score)

    # saves in context_dict['game_mode'] the readable game mode name of the game
    context_dict = game_mode_readable_name(game)

    # Create the Chart object
    cht = Chart(
        datasource = game_data,
        series_options =
          [{'options':{
              'type': 'column',
              'stacking': True},
            'terms':{
              'id': [
                'score']
              }}],
        chart_options =
          {'title': {
               'text': 'Statistics: ' + context_dict['game_mode']},
           'xAxis': {
                'title': {
                   'text': 'Games'}}},
        x_sortf_mapf_mts = (None, change_from_score_id_to_date, False))

    context_dict['chart'] = cht
    return context_dict

# at first I just wanna find all the users - later on I will search only for not friends
def get_not_friends_list(user, max_results=0, starts_with=''):

    friends = Friend.objects.friends(user)
    all_users = []
    #dispalying all the other users
    not_friends_list = []

    if starts_with != '':
        all_users = User.objects.exclude(username = user.username).filter(username__istartswith=starts_with)

    for user in all_users:
        if user not in friends:
           not_friends_list.append(user)

    if max_results > 0:
            if len(not_friends_list) > max_results:
                    not_friends_list = not_friends_list[:max_results]

    return not_friends_list


def suggest_friends(request):
    user = request.user
    not_friends_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']

    not_friends_list = get_not_friends_list(user, 8, starts_with)

    return render(request, 'keydash_app/friends_list_ajax.html', {'not_friends_list': not_friends_list })

