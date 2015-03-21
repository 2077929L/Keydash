from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.models import User
from keydash_app.models import Score, UserProfile, Game
from friendship.models import Friend, FriendshipRequest
from keydash_app.forms import UserForm, UserProfileForm
from chartit import DataPool, Chart

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

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
        game = Game.objects.get(game_mode = game_mode)
        context_dict.update( statistics_chart2(request, game) )
        user_scores_for_game_mode = Score.objects.filter(user = user, game = game).order_by('-score')

        # saving readable game mode names, later on used to display in template
        context_dict.update( game_mode_readable_name(game))
        context_dict['user_scores_for_game_mode'] = user_scores_for_game_mode

    else:
        context_dict.update( statistics_chart(request) )

    return render(request, 'keydash_app/statistics_personal.html', context_dict)

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
            return HttpResponseRedirect('/keydash/friends_keydash/')
        else:
            print profile_form.errors
    else:
        profile_form = UserProfileForm()

    return render(request, 'keydash_app/profile_registration.html', {'profile_form': profile_form })

def friends_keydash(request):
    context_dict = {}
    user = request.user
    friends = Friend.objects.friends(user)

    profiles = []
    for friend in friends:
        profile = UserProfile.objects.get(user = friend)
        profiles.append(profile)

    context_dict['profiles'] = profiles


    #dispalying all the other users
    other_users = []
    all_users = User.objects.exclude(username = user.username)
    for user in all_users:
        if user not in friends:
            other_users.append(user)

    context_dict['other_users'] = other_users
    print other_users

    return render(request, 'keydash_app/friends_keydash.html', context_dict)



def friends_requests_keydash(request):
    context_dict = {}
    user = request.user
    # List all unread friendship requests
    requests = FriendshipRequest.objects.filter(rejected__isnull=True, to_user=user)
    print requests
    context_dict['requests'] = requests
    return render(request, 'keydash_app/friends_requests_keydash.html', context_dict)


def friendship_accept_keydash(request, friendship_request_id):
    if request.method == 'POST':
        f_request = get_object_or_404(request.user.friendship_requests_received,id=friendship_request_id)
        f_request.accept()
        return HttpResponseRedirect('/keydash/friends_keydash')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


def friendship_reject_keydash(request, friendship_request_id):
    if request.method == 'POST':
        f_request = get_object_or_404(request.user.friendship_requests_received,id=friendship_request_id)
        f_request.delete()
        return HttpResponseRedirect('/keydash/friends_keydash')

    return redirect('friendship_requests_detail', friendship_request_id=friendship_request_id)


def game_mode_readable_name(game_mode):
    context_dict = {}
    if(game_mode.game_mode == 'eng_dict'):
        context_dict['game_mode'] = 'English Dictionary'
    elif(game_mode.game_mode == 'rand_alpha'):
        context_dict['game_mode'] = 'Random Alphanumeric'
    elif(game_mode.game_mode == 'rand_alpha_punc'):
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
                   'text': 'Games'}}})

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
                   'text': 'Games'}}})

    context_dict['chart'] = cht
    return context_dict



# at first I just wanna find all the users - later on I will search only for not friends
def get_not_friends_list(max_results=0, starts_with=''):
        not_friends_list = []
        if starts_with:
                not_friends_list = User.objects.filter(name__istartswith=starts_with)

        if max_results > 0:
                if len(not_friends_list) > max_results:
                        not_friends_list = not_friends_list[:max_results]

        return not_friends_list


def suggest_friends(request):

        not_friends_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']

        not_friends_list = get_not_friends_list(8, starts_with)

        return render(request, 'keydash_app/friends_list_ajax.html', {'not_friends_list': not_friends_list })
