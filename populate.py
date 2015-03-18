import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keydash_project.settings')

import django
django.setup()

from keydash_app.models import UserProfile, Game, Score
from django.contrib.auth.models import User

def populate():
    user1 = add_user('groucho','groucho@gmail.com','groucho')
    add_user_profile(user1, 1, 100, 100, 1000)
    user2 = add_user('harpo','harpo@gmail.com','harpo')
    add_user_profile(user2, 2, 90, 90, 900)
    user3 = add_user('chico','chico@gmail.com','chico')
    add_user_profile(user3, 3, 80, 80, 800)
    user4 = add_user('zeppo','zeppo@gmail.com','zeppo')
    add_user_profile(user4, 4, 70, 70, 700)

    game1 = add_games('eng_dict')
    game2 = add_games('rand_alpha')
    game3 = add_games('rand_alpha_punc')
    game4 = add_games('paragraph')

    add_score(user1, game1, 100, 90, 800)
    add_score(user1, game2, 90, 90, 700)
    add_score(user1, game3, 90, 90, 700)
    add_score(user1, game4, 90, 90, 700)
    add_score(user2, game1, 100, 100, 900)
    add_score(user2, game2, 10, 10, 20)
    add_score(user2, game3, 80, 100, 500)
    add_score(user2, game4, 0, 0, 0)
    add_score(user2, game4, 1, 100, 50)
    add_score(user3, game1, 200, 100, 1500)
    add_score(user3, game1, 100, 100, 910)
    add_score(user3, game2, 150, 100, 1200)
    add_score(user3, game3, 190, 100, 1400)
    add_score(user3, game2, 100, 20, 80)
    add_score(user4, game1, 100, 100, 800)
    add_score(user4, game1, 190, 20, 160)
    add_score(user4, game3, 140, 100, 1000)
    add_score(user4, game4, 90, 100, 600)
    add_score(user4, game4, 10, 50, 50)


def add_user(username, email, password):
    user = User.objects.get_or_create(username=username, email=email)[0]
    user.set_password(password)
    user.save()
    return user

def add_user_profile(user, ranking_position, wpm_highest, accuracy_highest, score_highest):
    userprofile = UserProfile.objects.get_or_create(user=user,
                                                    ranking_position=ranking_position,
                                                    wpm_highest=wpm_highest,
                                                    accuracy_highest=accuracy_highest,
                                                    score_highest = score_highest)[0]
    return userprofile

def add_games(game_mode):
    game = Game.objects.get_or_create(game_mode=game_mode)[0]
    return game

def add_score(user, game, wpm, accuracy, score):
    score = Score.objects.get_or_create(user=user,
                                        game=game,
                                        wpm=wpm,
                                        accuracy=accuracy,
                                        score=score)[0]
    return score

if __name__ == '__main__':
    print "Starting Keydash population script..."
    populate()